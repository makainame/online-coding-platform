from datetime import datetime

from sqlalchemy.orm import Session

from .advanced_python_problems import ADVANCED_PYTHON_PROBLEMS
from .curriculum_problems import CURRICULUM_PROBLEMS
from .curriculum_problems_extra import CURRICULUM_EXTRA_PROBLEMS
from .models import Problem, TestCase, User
from .sample_problems import PYTHON_PROBLEMS
from .security import hash_password


def seed_data(db: Session) -> None:
    if db.query(User).count() == 0:
        db.add_all(
            [
                User(
                    username="student",
                    password_hash=hash_password("student123"),
                    role="student",
                    email="student@example.com",
                ),
                User(
                    username="teacher",
                    password_hash=hash_password("teacher123"),
                    role="teacher",
                    email="teacher@example.com",
                ),
            ]
        )
        db.commit()

    teacher = db.query(User).filter(User.username == "teacher").first()
    existing_titles = {title for (title,) in db.query(Problem.title).all()}

    for item in [
        *PYTHON_PROBLEMS,
        *ADVANCED_PYTHON_PROBLEMS,
        *CURRICULUM_PROBLEMS,
        *CURRICULUM_EXTRA_PROBLEMS,
    ]:
        if item["title"] in existing_titles:
            continue

        problem = Problem(
            title=item["title"],
            description=item["description"],
            language=item.get("language", "python"),
            difficulty=item["difficulty"],
            tags=item["tags"],
            created_by=teacher.id if teacher else None,
            created_at=datetime.utcnow(),
        )
        db.add(problem)
        db.flush()

        for case in item["test_cases"]:
            db.add(
                TestCase(
                    problem_id=problem.id,
                    input=case["input"],
                    expected_output=case["expected_output"],
                    is_sample=True,
                )
            )
        existing_titles.add(item["title"])

    db.commit()
