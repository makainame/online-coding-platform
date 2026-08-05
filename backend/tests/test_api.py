import base64


def login(client, username="student", password="student123"):
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    return {"Authorization": f"Bearer {data['token']}"}


def test_register_login_and_me(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "new_student",
            "password": "secret123",
            "email": "new@example.com",
            "role": "student",
            "ai_provider": "deepseek",
            "ai_base_url": "https://api.deepseek.com/v1",
            "ai_model": "deepseek-chat",
            "ai_api_key": "test-key-123456",
            "avatar_base64": f"data:image/png;base64,{base64.b64encode(b'fake').decode()}",
        },
    )
    assert response.status_code == 200
    token = response.json()["token"]

    me = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["username"] == "new_student"
    assert me.json()["avatar"].startswith("/uploads/avatars/")


def test_student_requires_ai_key(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "no_ai_student",
            "password": "secret123",
            "role": "student",
        },
    )
    assert response.status_code == 400


def test_public_register_cannot_create_teacher(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "fake_teacher",
            "password": "secret123",
            "role": "teacher",
        },
    )
    assert response.status_code == 400


def test_teacher_register_with_code(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "new_teacher",
            "password": "secret123",
            "role": "teacher",
            "teacher_code": "teacher2026",
        },
    )
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "teacher"


def test_ai_settings_roundtrip(client):
    headers = login(client)
    initial = client.get("/api/ai/settings", headers=headers)
    assert initial.status_code == 200
    assert initial.json()["has_key"] is False

    updated = client.put(
        "/api/ai/settings",
        headers=headers,
        json={
            "provider": "deepseek",
            "api_key": "sk-test-1234567890",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
        },
    )
    assert updated.status_code == 200
    data = updated.json()
    assert data["has_key"] is True
    assert "sk-test-1234567890" not in str(data)
    assert data["masked_key"] == "sk-t...7890"


def test_ai_settings_delete(client):
    headers = login(client)
    client.put(
        "/api/ai/settings",
        headers=headers,
        json={
            "provider": "deepseek",
            "api_key": "sk-delete-123456",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
        },
    )

    deleted = client.delete("/api/ai/settings", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["has_key"] is False


def test_code_draft_save_and_get(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")

    saved = client.put(
        f"/api/drafts/{problem['id']}",
        headers=headers,
        json={
            "code": "print('draft')",
            "language": "python",
        },
    )
    assert saved.status_code == 200

    loaded = client.get(f"/api/drafts/{problem['id']}", headers=headers)
    assert loaded.status_code == 200
    assert loaded.json()["code"] == "print('draft')"


def test_student_full_flow(client):
    headers = login(client)

    problems = client.get("/api/problems", headers=headers)
    assert problems.status_code == 200
    problem = next(item for item in problems.json() if item["title"] == "两数之和")

    detail = client.get(f"/api/problems/{problem['id']}", headers=headers)
    assert detail.status_code == 200
    assert len(detail.json()["test_cases"]) >= 1

    code = "a, b = map(int, input().split())\nprint(a + b)"
    submission = client.post(
        "/api/submissions",
        headers=headers,
        json={
            "problem_id": problem["id"],
            "code": code,
            "language": "python",
        },
    )
    assert submission.status_code == 201
    submission_data = submission.json()
    assert submission_data["status"] == "accepted"
    assert len(submission_data["results"]) == 3

    feedback = client.post(
        f"/api/feedback/{submission_data['id']}",
        headers=headers,
    )
    assert feedback.status_code == 200
    feedback_data = feedback.json()
    assert feedback_data["provider"] == "local"
    assert feedback_data["score"] == 95.0


def test_wrong_answer_status(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")

    response = client.post(
        "/api/submissions",
        headers=headers,
        json={
            "problem_id": problem["id"],
            "code": "print(1)",
            "language": "python",
        },
    )
    assert response.status_code == 201
    assert response.json()["status"] == "wrong_answer"


def test_custom_execute(client):
    headers = login(client)
    response = client.post(
        "/api/execute",
        headers=headers,
        json={
            "problem_id": 1,
            "code": "print(input().strip())",
            "language": "python",
            "custom_input": "hello",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["results"][0]["actual_output"].strip() == "hello"


def test_execute_with_feedback(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")
    response = client.post(
        "/api/execute/feedback",
        headers=headers,
        json={
            "problem_id": problem["id"],
            "code": "a, b = map(int, input().split())\nprint(a + b)",
            "language": "python",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "local"
    assert data["feedback_text"]


def test_student_cannot_create_problem(client):
    headers = login(client)
    response = client.post(
        "/api/problems",
        headers=headers,
        json={
            "title": "越权题目",
            "description": "不应创建成功",
            "difficulty": "easy",
            "tags": "test",
            "test_cases": [],
        },
    )
    assert response.status_code == 403


def test_teacher_can_create_problem(client):
    headers = login(client, username="teacher", password="teacher123")
    response = client.post(
        "/api/problems",
        headers=headers,
        json={
            "title": "三个数相加",
            "description": "输入三个整数，输出它们的和。",
            "difficulty": "easy",
            "tags": "入门,数组",
            "test_cases": [
                {"input": "1 2 3", "expected_output": "6"},
                {"input": "10 20 30", "expected_output": "60"},
            ],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "三个数相加"
    assert len(data["test_cases"]) == 2


def test_teacher_import_problems(client):
    headers = login(client, username="teacher", password="teacher123")
    payload = [
        {
            "title": "导入题：求平方",
            "description": "输入 n，输出 n 的平方。",
            "language": "python",
            "difficulty": "easy",
            "tags": "导入,运算",
            "starter_code": "n = int(input())\nprint(n * n)\n",
            "test_cases": [
                {"input": "3", "expected_output": "9", "is_sample": True},
                {"input": "5", "expected_output": "25", "is_sample": True},
            ],
        }
    ]

    created = client.post("/api/problems/import", headers=headers, json=payload)
    assert created.status_code == 200
    assert created.json()["created"] == 1

    updated = client.post("/api/problems/import", headers=headers, json=payload)
    assert updated.status_code == 200
    assert updated.json()["updated"] == 1

    problems = client.get("/api/problems", headers=headers).json()
    imported = next(item for item in problems if item["title"] == "导入题：求平方")
    assert imported["language"] == "python"


def test_teacher_can_create_and_reset_student(client):
    headers = login(client, username="teacher", password="teacher123")

    created = client.post(
        "/api/admin/students",
        headers=headers,
        json={
            "username": "managed_student",
            "password": "init123456",
            "email": "managed@example.com",
        },
    )
    assert created.status_code == 201
    student_id = created.json()["id"]

    reset = client.put(
        f"/api/admin/students/{student_id}/password",
        headers=headers,
        json={"password": "newpass123"},
    )
    assert reset.status_code == 200

    students = client.get("/api/admin/students", headers=headers)
    assert students.status_code == 200
    assert any(item["username"] == "managed_student" for item in students.json())


def test_teacher_import_students(client):
    headers = login(client, username="teacher", password="teacher123")
    payload = [
        {
            "username": "batch_student_1",
            "password": "123456",
            "email": "batch1@example.com",
            "ai_api_key": "",
        },
        {
            "username": "batch_student_2",
            "password": "123456",
            "email": "batch2@example.com",
            "ai_api_key": "",
        },
    ]

    created = client.post("/api/admin/students/import", headers=headers, json=payload)
    assert created.status_code == 200
    assert created.json()["created"] == 2

    repeated = client.post("/api/admin/students/import", headers=headers, json=payload)
    assert repeated.status_code == 200
    assert repeated.json()["skipped"] == 2


def test_teacher_admin_statistics(client):
    student_headers = login(client)
    problems = client.get("/api/problems", headers=student_headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")
    client.post(
        "/api/submissions",
        headers=student_headers,
        json={
            "problem_id": problem["id"],
            "code": "a, b = map(int, input().split())\nprint(a + b)",
            "language": "python",
        },
    )

    teacher_headers = login(client, username="teacher", password="teacher123")
    stats = client.get("/api/admin/statistics", headers=teacher_headers)
    assert stats.status_code == 200
    assert stats.json()["total_submissions"] >= 1
    assert stats.json()["accepted_count"] >= 1


def test_student_cannot_manage_students(client):
    headers = login(client)
    response = client.get("/api/admin/students", headers=headers)
    assert response.status_code == 403


def test_my_statistics(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")
    code = "a, b = map(int, input().split())\nprint(a + b)"
    client.post(
        "/api/submissions",
        headers=headers,
        json={
            "problem_id": problem["id"],
            "code": code,
            "language": "python",
        },
    )

    response = client.get("/api/statistics/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_submissions"] == 1
    assert data["accepted_count"] == 1
