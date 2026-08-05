from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Feedback, Problem, Submission, User
from ..schemas import FeedbackOut
from ..security import get_current_user
from ..services.ai_feedback import generate_feedback


router = APIRouter(tags=["feedback"])


@router.get("/feedback/{submission_id}", response_model=FeedbackOut)
def get_feedback(
    submission_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Feedback:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    if submission.user_id != user.id and user.role != "teacher":
        raise HTTPException(status_code=403, detail="无权查看该提交")
    feedback = db.query(Feedback).filter(Feedback.submission_id == submission_id).first()
    if feedback is None:
        raise HTTPException(status_code=404, detail="反馈尚未生成")
    return feedback


@router.post("/feedback/{submission_id}", response_model=FeedbackOut)
def create_feedback(
    submission_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Feedback:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    if submission.user_id != user.id and user.role != "teacher":
        raise HTTPException(status_code=403, detail="无权查看该提交")
    problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")

    existing = db.query(Feedback).filter(Feedback.submission_id == submission_id).first()
    if existing:
        return existing

    from ..services.executor import execute_code

    result = execute_code(submission.code, submission.language, problem.test_cases)
    feedback = generate_feedback(db, submission, problem, result, user=user)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
