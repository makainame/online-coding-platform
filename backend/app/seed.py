from datetime import datetime

from sqlalchemy.orm import Session

from .advanced_python_problems import ADVANCED_PYTHON_PROBLEMS
from .case_study_problems import CASE_STUDY_PROBLEMS
from .cpp_problems import CPP_PROBLEMS
from .curriculum_problems import CURRICULUM_PROBLEMS
from .curriculum_problems_extra import CURRICULUM_EXTRA_PROBLEMS
from .java_problems import JAVA_PROBLEMS
from .javascript_problems import JAVASCRIPT_PROBLEMS
from .models import Exam, ExamProblem, Problem, TestCase, User
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
        *CASE_STUDY_PROBLEMS,
        *JAVASCRIPT_PROBLEMS,
        *JAVA_PROBLEMS,
        *CPP_PROBLEMS,
    ]:
        if item["title"] in existing_titles:
            continue

        problem = Problem(
            title=item["title"],
            description=item["description"],
            language=item.get("language", "python"),
            difficulty=item["difficulty"],
            tags=item["tags"],
            starter_code=item.get("starter_code"),
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

    _normalize_problem_meta(db)
    _seed_case_study_exam(db, teacher)


def _normalize_problem_meta(db: Session) -> None:
    for problem in db.query(Problem).all():
        tags = {tag.strip() for tag in problem.tags.split(",") if tag.strip()}
        if "案例检测" in tags:
            problem.question_type = "案例题"
        elif tags & {"print", "格式化", "f-string", "转义符", "注释", "输出"}:
            problem.question_type = "概念/输出题"
        elif problem.question_type == "编程题":
            problem.question_type = "编程题"

        if problem.score is None:
            problem.score = {
                "easy": 10,
                "medium": 15,
                "hard": 20,
            }.get(problem.difficulty, 10)
    db.commit()


def _seed_case_study_exam(db: Session, teacher: User | None) -> None:
    if teacher is None:
        return
    existing = (
        db.query(Exam)
        .filter(
            Exam.title == "Python 案例检测卷",
            Exam.created_by == teacher.id,
        )
        .first()
    )
    if existing is not None:
        return

    titles = [item["title"] for item in CASE_STUDY_PROBLEMS]
    problems = (
        db.query(Problem)
        .filter(
            Problem.title.in_(titles),
            Problem.language == "python",
        )
        .order_by(Problem.id)
        .all()
    )
    if len(problems) < len(titles):
        return

    exam = Exam(
        title="Python 案例检测卷",
        description="包含学生成绩分析、文本词频统计、商品库存管理三道综合案例题。",
        duration_minutes=60,
        class_id=None,
        status="draft",
        created_by=teacher.id,
    )
    db.add(exam)
    db.flush()
    for index, problem in enumerate(problems):
        db.add(
            ExamProblem(
                exam_id=exam.id,
                problem_id=problem.id,
                order_index=index,
            )
        )
    db.commit()
