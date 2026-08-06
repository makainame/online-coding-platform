from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..ai_crypto import encrypt_api_key
from ..database import get_db
from ..models import AiSetting, ClassGroup, Problem, Submission, User
from ..schemas import (
    AdminStatsOut,
    AdminStudentStatOut,
    DailyStatOut,
    PasswordReset,
    ScoreExportOut,
    ScoreExportProblem,
    StudentCreate,
    StudentImportResult,
    StudentScoreExportRow,
    StudentOut,
)
from ..security import hash_password, require_teacher


router = APIRouter(tags=["students"])


@router.get("/admin/statistics", response_model=AdminStatsOut)
def admin_statistics(
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> AdminStatsOut:
    students = (
        db.query(User)
        .filter(User.role == "student")
        .order_by(User.id)
        .all()
    )
    submissions = db.query(Submission).all()
    total = len(submissions)
    accepted_count = sum(1 for item in submissions if item.status == "accepted")
    wrong_count = sum(1 for item in submissions if item.status == "wrong_answer")
    error_count = sum(1 for item in submissions if item.status == "error")
    pass_rate = round(accepted_count / total * 100, 1) if total else 0.0

    daily_map: dict[str, dict[str, int]] = {}
    for item in submissions:
        if not item.created_at:
            continue
        day = item.created_at.date().isoformat()
        entry = daily_map.setdefault(day, {"submissions": 0, "accepted": 0})
        entry["submissions"] += 1
        if item.status == "accepted":
            entry["accepted"] += 1

    today_date = datetime.utcnow().date()
    dates = [
        (today_date - timedelta(days=offset)).isoformat()
        for offset in range(6, -1, -1)
    ]
    daily = [
        DailyStatOut(
            date=date,
            submissions=daily_map.get(date, {}).get("submissions", 0),
            accepted=daily_map.get(date, {}).get("accepted", 0),
        )
        for date in dates
    ]

    student_rows = []
    class_name_by_id = _class_name_map(db, students)
    for student in students:
        _student_counts(db, student)
        student_rows.append(
            AdminStudentStatOut(
                user_id=student.id,
                username=student.username,
                email=student.email,
                class_id=student.class_id,
                class_name=class_name_by_id.get(student.class_id, ""),
                submission_count=student.submission_count,
                accepted_count=student.accepted_count,
                pass_rate=round(
                    student.accepted_count / student.submission_count * 100,
                    1,
                )
                if student.submission_count
                else 0.0,
            )
        )

    return AdminStatsOut(
        total_students=len(students),
        total_submissions=total,
        accepted_count=accepted_count,
        wrong_count=wrong_count,
        error_count=error_count,
        pass_rate=pass_rate,
        students=student_rows,
        daily=daily,
    )


@router.get("/admin/statistics/export", response_model=ScoreExportOut)
def export_student_scores(
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ScoreExportOut:
    students = (
        db.query(User)
        .filter(User.role == "student")
        .order_by(User.id)
        .all()
    )
    problems = db.query(Problem).order_by(Problem.id).all()
    submissions = db.query(Submission).all()

    student_problem_stats: dict[int, dict[int, dict[str, int]]] = {}
    for submission in submissions:
        student_stats = student_problem_stats.setdefault(submission.user_id, {})
        stats = student_stats.setdefault(
            submission.problem_id,
            {"submissions": 0, "accepted": 0},
        )
        stats["submissions"] += 1
        if submission.status == "accepted":
            stats["accepted"] += 1

    rows = []
    class_name_by_id = _class_name_map(db, students)
    for student in students:
        stats_by_problem = student_problem_stats.get(student.id, {})
        total = sum(item["submissions"] for item in stats_by_problem.values())
        accepted = sum(item["accepted"] for item in stats_by_problem.values())
        problem_statuses = {}
        for problem in problems:
            stats = stats_by_problem.get(problem.id, {"submissions": 0, "accepted": 0})
            if stats["accepted"] > 0:
                problem_statuses[str(problem.id)] = "通过"
            elif stats["submissions"] > 0:
                problem_statuses[str(problem.id)] = "已提交未通过"
            else:
                problem_statuses[str(problem.id)] = "未作答"
        rows.append(
            StudentScoreExportRow(
                username=student.username,
                email=student.email,
                class_id=student.class_id,
                class_name=class_name_by_id.get(student.class_id, ""),
                submission_count=total,
                accepted_count=accepted,
                pass_rate=round(accepted / total * 100, 1) if total else 0.0,
                problem_statuses=problem_statuses,
            )
        )

    return ScoreExportOut(
        problems=[
            ScoreExportProblem(
                problem_id=problem.id,
                title=problem.title,
                language=problem.language,
            )
            for problem in problems
        ],
        rows=rows,
    )


def _student_counts(db: Session, student: User) -> None:
    student.submission_count = (
        db.query(func.count(Submission.id))
        .filter(Submission.user_id == student.id)
        .scalar()
        or 0
    )
    student.accepted_count = (
        db.query(func.count(Submission.id))
        .filter(
            Submission.user_id == student.id,
            Submission.status == "accepted",
        )
        .scalar()
        or 0
    )


def _class_name_map(db: Session, students: list[User]) -> dict[int, str]:
    class_ids = {student.class_id for student in students if student.class_id}
    if not class_ids:
        return {}
    return {
        class_group.id: class_group.name
        for class_group in db.query(ClassGroup)
        .filter(ClassGroup.id.in_(class_ids))
        .all()
    }


def _build_student(db: Session, payload: StudentCreate) -> User:
    student = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="student",
    )
    db.add(student)
    db.flush()
    if payload.ai_api_key:
        db.add(
            AiSetting(
                user_id=student.id,
                provider=payload.ai_provider,
                encrypted_api_key=encrypt_api_key(payload.ai_api_key),
                base_url=payload.ai_base_url,
                model=payload.ai_model,
            )
        )
    return student


@router.get("/admin/students", response_model=list[StudentOut])
def list_students(
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> list[User]:
    students = (
        db.query(User)
        .filter(User.role == "student")
        .order_by(User.id)
        .all()
    )
    class_name_by_id = _class_name_map(db, students)
    for student in students:
        _student_counts(db, student)
        student.class_name = class_name_by_id.get(student.class_id, "")
    return students


@router.post(
    "/admin/students",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> User:
    conditions = [User.username == payload.username]
    if payload.email:
        conditions.append(User.email == payload.email)
    existing = db.query(User).filter(or_(*conditions)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在",
        )

    student = _build_student(db, payload)
    db.commit()
    db.refresh(student)
    _student_counts(db, student)
    return student


@router.post("/admin/students/import", response_model=StudentImportResult)
def import_students(
    payload: list[StudentCreate],
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> StudentImportResult:
    created = 0
    skipped = 0
    seen: set[str] = set()

    for item in payload:
        if item.username in seen:
            skipped += 1
            continue
        conditions = [User.username == item.username]
        if item.email:
            conditions.append(User.email == item.email)
        existing = db.query(User).filter(or_(*conditions)).first()
        if existing:
            skipped += 1
            continue
        _build_student(db, item)
        seen.add(item.username)
        created += 1

    db.commit()
    return StudentImportResult(
        created=created,
        skipped=skipped,
        total=len(payload),
    )


@router.put("/admin/students/{student_id}/password", response_model=StudentOut)
def reset_student_password(
    student_id: int,
    payload: PasswordReset,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> User:
    student = (
        db.query(User)
        .filter(User.id == student_id, User.role == "student")
        .first()
    )
    if student is None:
        raise HTTPException(status_code=404, detail="学生账号不存在")
    student.password_hash = hash_password(payload.password)
    db.commit()
    db.refresh(student)
    _student_counts(db, student)
    return student
