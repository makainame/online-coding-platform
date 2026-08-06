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


def test_javascript_problem_is_seeded_with_starter_code(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    js_problem = next(
        item
        for item in problems
        if item["title"] == "JavaScript 两数之和"
    )

    detail = client.get(f"/api/problems/{js_problem['id']}", headers=headers)
    assert detail.status_code == 200
    data = detail.json()
    assert data["language"] == "javascript"
    assert "readFileSync" in data["starter_code"]


def test_java_problem_is_seeded_with_starter_code(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    java_problem = next(
        item
        for item in problems
        if item["title"] == "Java 两数之和"
    )

    detail = client.get(f"/api/problems/{java_problem['id']}", headers=headers)
    assert detail.status_code == 200
    data = detail.json()
    assert data["language"] == "java"
    assert "public class Main" in data["starter_code"]


def test_cpp_problem_is_seeded_with_starter_code(client):
    headers = login(client)
    problems = client.get("/api/problems", headers=headers).json()
    cpp_problem = next(
        item
        for item in problems
        if item["title"] == "C++ 两数之和"
    )

    detail = client.get(f"/api/problems/{cpp_problem['id']}", headers=headers)
    assert detail.status_code == 200
    data = detail.json()
    assert data["language"] == "cpp"
    assert "#include <iostream>" in data["starter_code"]


def test_case_study_paper_is_seeded(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    problems = client.get("/api/problems", headers=teacher_headers).json()
    case_titles = {
        "案例：学生成绩分析",
        "案例：文本词频统计",
        "案例：商品库存管理",
    }
    assert case_titles.issubset({item["title"] for item in problems})

    exams = client.get("/api/admin/exams", headers=teacher_headers).json()
    paper = next(
        item
        for item in exams
        if item["title"] == "Python 案例检测卷"
    )
    assert paper["status"] == "draft"
    assert paper["problem_count"] == 3


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


def test_teacher_delete_problem_with_related_records(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    created = client.post(
        "/api/problems",
        headers=teacher_headers,
        json={
            "title": "删除测试题",
            "description": "输出固定结果。",
            "difficulty": "easy",
            "tags": "测试",
            "test_cases": [
                {"input": "1", "expected_output": "2", "is_sample": True},
            ],
        },
    )
    assert created.status_code == 201
    problem_id = created.json()["id"]

    student_headers = login(client)
    client.put(
        f"/api/drafts/{problem_id}",
        headers=student_headers,
        json={"code": "print(2)", "language": "python"},
    )
    submission = client.post(
        "/api/submissions",
        headers=student_headers,
        json={
            "problem_id": problem_id,
            "code": "print(2)",
            "language": "python",
        },
    )
    assert submission.status_code == 201
    client.post(
        f"/api/feedback/{submission.json()['id']}",
        headers=student_headers,
    )

    deleted = client.delete(
        f"/api/problems/{problem_id}",
        headers=teacher_headers,
    )
    assert deleted.status_code == 204

    problems = client.get("/api/problems", headers=student_headers).json()
    assert not any(item["id"] == problem_id for item in problems)


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


def test_teacher_class_management_and_assignment(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    created = client.post(
        "/api/admin/classes",
        headers=teacher_headers,
        json={"name": "Python 一班"},
    )
    assert created.status_code == 201
    class_id = created.json()["id"]

    duplicate = client.post(
        "/api/admin/classes",
        headers=teacher_headers,
        json={"name": "Python 一班"},
    )
    assert duplicate.status_code == 400

    student = client.post(
        "/api/admin/students",
        headers=teacher_headers,
        json={
            "username": "class_student",
            "password": "class123456",
            "email": "class@example.com",
        },
    )
    assert student.status_code == 201
    student_id = student.json()["id"]

    assigned = client.put(
        f"/api/admin/students/{student_id}/class",
        headers=teacher_headers,
        json={"class_id": class_id},
    )
    assert assigned.status_code == 200
    assert assigned.json()["class_name"] == "Python 一班"

    classes = client.get("/api/admin/classes", headers=teacher_headers)
    assert classes.status_code == 200
    class_row = next(item for item in classes.json() if item["id"] == class_id)
    assert class_row["student_count"] == 1

    students = client.get("/api/admin/students", headers=teacher_headers)
    student_row = next(
        item for item in students.json() if item["id"] == student_id
    )
    assert student_row["class_id"] == class_id
    assert student_row["class_name"] == "Python 一班"

    renamed = client.put(
        f"/api/admin/classes/{class_id}",
        headers=teacher_headers,
        json={"name": "Python 二班"},
    )
    assert renamed.status_code == 200
    assert renamed.json()["name"] == "Python 二班"

    deleted = client.delete(
        f"/api/admin/classes/{class_id}",
        headers=teacher_headers,
    )
    assert deleted.status_code == 204

    students_after_delete = client.get(
        "/api/admin/students",
        headers=teacher_headers,
    )
    student_after_delete = next(
        item for item in students_after_delete.json() if item["id"] == student_id
    )
    assert student_after_delete["class_id"] is None


def test_teacher_class_appears_in_stats_and_export(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    class_group = client.post(
        "/api/admin/classes",
        headers=teacher_headers,
        json={"name": "统计一班"},
    ).json()
    student = client.post(
        "/api/admin/students",
        headers=teacher_headers,
        json={
            "username": "stats_student",
            "password": "stats123456",
            "email": "stats@example.com",
        },
    ).json()
    client.put(
        f"/api/admin/students/{student['id']}/class",
        headers=teacher_headers,
        json={"class_id": class_group["id"]},
    )

    stats = client.get("/api/admin/statistics", headers=teacher_headers)
    assert stats.status_code == 200
    stats_row = next(
        item
        for item in stats.json()["students"]
        if item["username"] == "stats_student"
    )
    assert stats_row["class_name"] == "统计一班"

    exported = client.get("/api/admin/statistics/export", headers=teacher_headers)
    assert exported.status_code == 200
    export_row = next(
        item
        for item in exported.json()["rows"]
        if item["username"] == "stats_student"
    )
    assert export_row["class_name"] == "统计一班"


def test_student_cannot_manage_classes(client):
    headers = login(client)
    response = client.get("/api/admin/classes", headers=headers)
    assert response.status_code == 403


def test_teacher_can_create_update_and_delete_exam(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    problems = client.get("/api/problems", headers=teacher_headers).json()
    problem_ids = [item["id"] for item in problems[:3]]

    created = client.post(
        "/api/admin/exams",
        headers=teacher_headers,
        json={
            "title": "Python 阶段测试",
            "description": "第一阶段考试",
            "duration_minutes": 60,
            "status": "published",
            "problem_ids": problem_ids,
        },
    )
    assert created.status_code == 201
    exam_id = created.json()["id"]
    assert created.json()["problem_count"] == 3

    detail = client.get(
        f"/api/admin/exams/{exam_id}",
        headers=teacher_headers,
    )
    assert detail.status_code == 200
    assert len(detail.json()["problems"]) == 3

    updated = client.put(
        f"/api/admin/exams/{exam_id}",
        headers=teacher_headers,
        json={
            "title": "Python 阶段测试改",
            "problem_ids": problem_ids[:2],
        },
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Python 阶段测试改"
    assert updated.json()["problem_count"] == 2

    deleted = client.delete(
        f"/api/admin/exams/{exam_id}",
        headers=teacher_headers,
    )
    assert deleted.status_code == 204


def test_exam_title_cannot_be_numeric_only(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    problems = client.get("/api/problems", headers=teacher_headers).json()
    problem_ids = [item["id"] for item in problems[:1]]

    response = client.post(
        "/api/admin/exams",
        headers=teacher_headers,
        json={
            "title": "333",
            "description": "无效标题",
            "duration_minutes": 30,
            "status": "draft",
            "problem_ids": problem_ids,
        },
    )
    assert response.status_code == 400
    assert "有意义的名称" in response.json()["detail"]


def test_teacher_auto_create_exam_by_knowledge_points(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    created = client.post(
        "/api/admin/exams/auto",
        headers=teacher_headers,
        json={
            "title": "Python 知识点自动卷",
            "description": "按知识点自动组卷",
            "duration_minutes": 40,
            "status": "draft",
            "knowledge_points": ["Day01", "字符串"],
            "count_per_point": 2,
            "difficulty": "easy",
            "language": "python",
        },
    )
    assert created.status_code == 201
    exam_id = created.json()["id"]
    assert 1 <= created.json()["problem_count"] <= 4
    assert all(
        item["language"] == "python"
        for item in created.json()["problems"]
    )

    updated = client.put(
        f"/api/admin/exams/{exam_id}/auto-select",
        headers=teacher_headers,
        json={
            "knowledge_points": ["列表"],
            "count_per_point": 2,
            "difficulty": "easy",
            "language": "python",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["problem_count"] >= 1


def test_teacher_can_create_standard_stage_exam(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    created = client.post(
        "/api/admin/exams/stage",
        headers=teacher_headers,
        json={
            "stage": "stage1",
            "target_count": 10,
            "duration_minutes": 45,
            "status": "draft",
        },
    )
    assert created.status_code == 201
    data = created.json()
    assert data["title"] == "Python 阶段检测一（Day01-Day03）"
    assert 5 <= data["problem_count"] <= 10
    assert sum(item["score"] or 0 for item in data["problems"]) == 100
    assert all((item["score"] or 0) == 10 for item in data["problems"])
    assert any(item["question_type"] for item in data["problems"])
    assert all(
        item["starter_code"].startswith("# 请根据题目要求完成代码")
        for item in data["problems"]
    )
    assert all("示例" in item["description"] for item in data["problems"])
    assert all(item["test_cases"] for item in data["problems"])

    titles = [item["title"] for item in data["problems"]]
    assert len(titles) == len(set(titles))
    tags = ",".join(item["tags"] for item in data["problems"])
    assert any(tag in tags for tag in ("Day01", "Day02", "Day03"))


def test_student_exam_flow_and_score(client):
    student_headers = login(client)
    problems = client.get("/api/problems", headers=student_headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")

    teacher_headers = login(client, username="teacher", password="teacher123")
    exam = client.post(
        "/api/admin/exams",
        headers=teacher_headers,
        json={
            "title": "学生考试流程",
            "description": "流程验证",
            "duration_minutes": 30,
            "status": "published",
            "problem_ids": [problem["id"]],
        },
    ).json()

    started = client.post(
        f"/api/exams/{exam['id']}/start",
        headers=student_headers,
    )
    assert started.status_code == 200
    assert started.json()["status"] == "in_progress"

    submitted = client.post(
        "/api/submissions",
        headers=student_headers,
        json={
            "problem_id": problem["id"],
            "code": "a, b = map(int, input().split())\nprint(a + b)",
            "language": "python",
            "exam_id": exam["id"],
        },
    )
    assert submitted.status_code == 201
    assert submitted.json()["status"] == "accepted"
    assert submitted.json()["exam_id"] == exam["id"]

    finished = client.post(
        f"/api/exams/{exam['id']}/submit",
        headers=student_headers,
    )
    assert finished.status_code == 200
    assert finished.json()["score"] == 100
    assert finished.json()["accepted_problems"] == 1
    assert finished.json()["total_problems"] == 1

    detail = client.get(
        f"/api/exams/{exam['id']}",
        headers=student_headers,
    )
    assert detail.status_code == 200
    assert detail.json()["attempt_status"] == "submitted"
    assert detail.json()["results"][str(problem["id"])] == "accepted"
    assert all(
        not item.get("test_cases")
        for item in detail.json()["problems"]
    )

    results = client.get(
        f"/api/admin/exams/{exam['id']}/results",
        headers=teacher_headers,
    )
    assert results.status_code == 200
    assert results.json()[0]["username"] == "student"
    assert results.json()[0]["score"] == 100
    assert results.json()[0]["problem_statuses"][str(problem["id"])] == "accepted"

    exported = client.get(
        f"/api/admin/exams/{exam['id']}/results/export",
        headers=teacher_headers,
    )
    assert exported.status_code == 200
    assert exported.json()[0]["problem_statuses"][str(problem["id"])] == "accepted"


def test_student_exam_submission_requires_start(client):
    student_headers = login(client)
    problems = client.get("/api/problems", headers=student_headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")
    teacher_headers = login(client, username="teacher", password="teacher123")
    exam = client.post(
        "/api/admin/exams",
        headers=teacher_headers,
        json={
            "title": "未开始考试",
            "description": "未开始",
            "duration_minutes": 30,
            "status": "published",
            "problem_ids": [problem["id"]],
        },
    ).json()

    response = client.post(
        "/api/submissions",
        headers=student_headers,
        json={
            "problem_id": problem["id"],
            "code": "print(1)",
            "language": "python",
            "exam_id": exam["id"],
        },
    )
    assert response.status_code == 400


def test_exam_published_by_class_only_reaches_that_class(client):
    teacher_headers = login(client, username="teacher", password="teacher123")
    class_group = client.post(
        "/api/admin/classes",
        headers=teacher_headers,
        json={"name": "考试一班"},
    ).json()
    inside_student = client.post(
        "/api/admin/students",
        headers=teacher_headers,
        json={
            "username": "inside_student",
            "password": "inside123456",
            "email": "inside@example.com",
        },
    ).json()
    client.put(
        f"/api/admin/students/{inside_student['id']}/class",
        headers=teacher_headers,
        json={"class_id": class_group["id"]},
    )
    outside_student = client.post(
        "/api/admin/students",
        headers=teacher_headers,
        json={
            "username": "outside_student",
            "password": "outside123456",
            "email": "outside@example.com",
        },
    ).json()
    problems = client.get("/api/problems", headers=teacher_headers).json()
    problem = next(item for item in problems if item["title"] == "两数之和")
    exam = client.post(
        "/api/admin/exams",
        headers=teacher_headers,
        json={
            "title": "一班专项考试",
            "description": "按班发布",
            "duration_minutes": 30,
            "class_id": class_group["id"],
            "status": "published",
            "problem_ids": [problem["id"]],
        },
    ).json()

    inside_headers = login(client, "inside_student", "inside123456")
    inside_exams = client.get("/api/exams", headers=inside_headers).json()
    assert any(item["id"] == exam["id"] for item in inside_exams)

    outside_headers = login(client, "outside_student", "outside123456")
    outside_exams = client.get("/api/exams", headers=outside_headers).json()
    assert not any(item["id"] == exam["id"] for item in outside_exams)
    forbidden = client.get(
        f"/api/exams/{exam['id']}",
        headers=outside_headers,
    )
    assert forbidden.status_code == 403


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


def test_teacher_export_student_scores(client):
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
    exported = client.get(
        "/api/admin/statistics/export",
        headers=teacher_headers,
    )
    assert exported.status_code == 200
    data = exported.json()
    assert data["problems"]
    student_row = next(
        item for item in data["rows"] if item["username"] == "student"
    )
    assert student_row["submission_count"] == 1
    assert student_row["accepted_count"] == 1
    assert student_row["problem_statuses"][str(problem["id"])] == "通过"


def test_student_cannot_export_scores(client):
    headers = login(client)
    response = client.get("/api/admin/statistics/export", headers=headers)
    assert response.status_code == 403


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
