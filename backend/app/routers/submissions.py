from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ClassGroup, Exam, ExamAttempt, ExamProblem, Problem, Submission, User
from ..schemas import (
    DailySubmissionOut,
    DailySubmissionStudentOut,
    ExecuteRequest,
    ExecuteResultOut,
    FeedbackOut,
    SubmissionCreate,
    SubmissionDetail,
    SubmissionListOut,
    SubmissionOut,
)
from ..security import get_current_user, require_teacher
from ..services.ai_feedback import generate_feedback
from ..services.executor import execute_code, execute_custom


router = APIRouter(tags=["submissions"])


def _local_date_range(date: str) -> tuple[datetime, datetime]:
    try:
        local_midnight = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="日期格式不正确，应为 YYYY-MM-DD",
        ) from exc
    start = local_midnight - timedelta(hours=8)
    return start, start + timedelta(days=1)


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


@router.get("/submissions/my", response_model=list[SubmissionOut])
def my_submissions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.user_id == user.id)
        .order_by(Submission.id.desc())
        .limit(100)
        .all()
    )


@router.get("/submissions", response_model=list[SubmissionListOut])
def list_submissions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    date: str | None = None,
):
    query = (
        db.query(Submission, User.username, Problem.title)
        .join(User, User.id == Submission.user_id)
        .join(Problem, Problem.id == Submission.problem_id)
    )
    if user.role != "teacher":
        query = query.filter(Submission.user_id == user.id)
    if date is not None:
        start, end = _local_date_range(date)
        query = query.filter(
            Submission.created_at >= start,
            Submission.created_at < end,
        )
    rows = (
        query.order_by(Submission.id.desc())
        .limit(1000)
        .all()
    )
    return [
        SubmissionListOut(
            **SubmissionOut.model_validate(submission).model_dump(),
            username=username,
            problem_title=problem_title,
        )
        for submission, username, problem_title in rows
    ]


@router.get("/admin/submissions/daily", response_model=DailySubmissionOut)
def daily_submissions(
    date: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> DailySubmissionOut:
    start, end = _local_date_range(date)
    students = (
        db.query(User)
        .filter(User.role == "student")
        .order_by(User.class_id, User.username)
        .all()
    )
    submissions = (
        db.query(Submission)
        .filter(
            Submission.created_at >= start,
            Submission.created_at < end,
        )
        .order_by(Submission.created_at, Submission.id)
        .all()
    )
    class_name_by_id = _class_name_map(db, students)
    grouped: dict[int, list[Submission]] = {}
    for submission in submissions:
        grouped.setdefault(submission.user_id, []).append(submission)

    rows = []
    for student in students:
        records = grouped.get(student.id, [])
        latest = records[-1] if records else None
        rows.append(
            DailySubmissionStudentOut(
                user_id=student.id,
                username=student.username,
                email=student.email,
                class_name=class_name_by_id.get(student.class_id, ""),
                submission_count=len(records),
                accepted_count=sum(
                    1 for record in records if record.status == "accepted"
                ),
                latest_status=latest.status if latest else "",
                latest_time=latest.created_at if latest else None,
            )
        )

    submitted_students = sum(1 for row in rows if row.submission_count > 0)
    return DailySubmissionOut(
        date=date,
        total_students=len(rows),
        submitted_students=submitted_students,
        not_submitted_students=len(rows) - submitted_students,
        students=rows,
    )


@router.post("/execute", response_model=ExecuteResultOut)
def execute(
    payload: ExecuteRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ExecuteResultOut:
    problem = db.query(Problem).filter(Problem.id == payload.problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    if payload.mode == "run" or payload.custom_input is not None:
        return execute_custom(
            payload.code,
            payload.language,
            payload.custom_input or "",
        )
    return execute_code(payload.code, payload.language, problem.test_cases)


@router.post("/execute/feedback", response_model=FeedbackOut)
def execute_with_feedback(
    payload: ExecuteRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    problem = db.query(Problem).filter(Problem.id == payload.problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")

    if payload.mode == "run" or payload.custom_input is not None:
        result = execute_custom(
            payload.code,
            payload.language,
            payload.custom_input or "",
        )
    else:
        result = execute_code(payload.code, payload.language, problem.test_cases)

    submission = Submission(
        user_id=user.id,
        problem_id=payload.problem_id,
        code=payload.code,
        language=payload.language,
        status=result.status,
        execution_time=result.execution_time,
        actual_output="\n".join(item.actual_output for item in result.results if item.actual_output),
        error_message=result.error_message,
    )
    feedback = generate_feedback(
        db,
        submission,
        problem,
        result,
        user=user,
        run_mode=payload.mode == "run" or payload.custom_input is not None,
    )
    feedback.id = 0
    feedback.submission_id = 0
    return feedback


@router.post("/submissions", response_model=SubmissionDetail, status_code=status.HTTP_201_CREATED)
def create_submission(
    payload: SubmissionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Submission:
    problem = db.query(Problem).filter(Problem.id == payload.problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")

    if payload.exam_id is not None:
        exam = db.query(Exam).filter(Exam.id == payload.exam_id).first()
        if exam is None:
            raise HTTPException(status_code=404, detail="考试不存在")
        attempt = (
            db.query(ExamAttempt)
            .filter(
                ExamAttempt.exam_id == payload.exam_id,
                ExamAttempt.user_id == user.id,
            )
            .first()
        )
        if attempt is None or attempt.status != "in_progress":
            raise HTTPException(status_code=400, detail="考试尚未开始或已提交")
        if (
            attempt.started_at
            and datetime.utcnow()
            > attempt.started_at + timedelta(minutes=exam.duration_minutes)
        ):
            raise HTTPException(status_code=400, detail="考试时间已结束，无法继续提交")
        problem_link = (
            db.query(ExamProblem)
            .filter(
                ExamProblem.exam_id == payload.exam_id,
                ExamProblem.problem_id == payload.problem_id,
            )
            .first()
        )
        if problem_link is None:
            raise HTTPException(status_code=400, detail="该题目不属于本次考试")

    result = execute_code(payload.code, payload.language, problem.test_cases)
    submission = Submission(
        user_id=user.id,
        problem_id=payload.problem_id,
        exam_id=payload.exam_id,
        code=payload.code,
        language=payload.language,
        status=result.status,
        execution_time=result.execution_time,
        actual_output="\n".join(item.actual_output for item in result.results if item.actual_output),
        error_message=result.error_message,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    submission.results = result.results  # type: ignore[attr-defined]
    return submission


@router.get("/submissions/{submission_id}", response_model=SubmissionDetail)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Submission:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    if submission.user_id != user.id and user.role != "teacher":
        raise HTTPException(status_code=403, detail="无权查看该提交")
    return submission
