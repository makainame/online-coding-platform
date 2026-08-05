from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CodeDraft, Problem, User
from ..schemas import CodeDraftOut, CodeDraftSave
from ..security import get_current_user


router = APIRouter(tags=["drafts"])


@router.get("/drafts/{problem_id}", response_model=CodeDraftOut)
def get_draft(
    problem_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CodeDraftOut:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")

    draft = (
        db.query(CodeDraft)
        .filter(
            CodeDraft.user_id == user.id,
            CodeDraft.problem_id == problem_id,
        )
        .first()
    )
    if draft is None:
        return CodeDraftOut(code="", language=problem.language, updated_at=None)
    return CodeDraftOut(
        code=draft.code,
        language=draft.language,
        updated_at=draft.updated_at,
    )


@router.put("/drafts/{problem_id}", response_model=CodeDraftOut)
def save_draft(
    problem_id: int,
    payload: CodeDraftSave,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CodeDraftOut:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")

    draft = (
        db.query(CodeDraft)
        .filter(
            CodeDraft.user_id == user.id,
            CodeDraft.problem_id == problem_id,
        )
        .first()
    )
    if draft is None:
        draft = CodeDraft(
            user_id=user.id,
            problem_id=problem_id,
            code=payload.code,
            language=payload.language,
        )
        db.add(draft)
    else:
        draft.code = payload.code
        draft.language = payload.language
    db.commit()
    db.refresh(draft)
    return CodeDraftOut(
        code=draft.code,
        language=draft.language,
        updated_at=draft.updated_at,
    )
