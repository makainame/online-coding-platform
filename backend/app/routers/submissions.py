from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Problem, Submission, User
from ..schemas import (
    ExecuteRequest,
    ExecuteResultOut,
    FeedbackOut,
    SubmissionCreate,
    SubmissionDetail,
    SubmissionOut,
)
from ..security import get_current_user
from ..services.ai_feedback import generate_feedback
from ..services.executor import execute_code, execute_custom


router = APIRouter(tags=["submissions"])


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


@router.post("/execute", response_model=ExecuteResultOut)
def execute(
    payload: ExecuteRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ExecuteResultOut:
    problem = db.query(Problem).filter(Problem.id == payload.problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    if payload.custom_input is not None:
        return execute_custom(payload.code, payload.language, payload.custom_input)
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

    if payload.custom_input is not None:
        result = execute_custom(payload.code, payload.language, payload.custom_input)
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
    feedback = generate_feedback(db, submission, problem, result, user=user)
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
