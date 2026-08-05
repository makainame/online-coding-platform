import re

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CodeDraft, Feedback, Problem, Submission, TestCase, User
from ..schemas import (
    ProblemCreate,
    ProblemDetail,
    ProblemImportResult,
    ProblemOut,
    ProblemUpdate,
    TestCaseOut,
)
from ..security import get_current_user, require_teacher
from ..starter_codes import get_starter_code


router = APIRouter(tags=["problems"])


def _teaching_rank(problem: Problem) -> tuple:
    for tag in problem.tags.split(","):
        match = re.fullmatch(r"(进阶)?Day(\d+)", tag)
        if match:
            return (
                0 if not match.group(1) else 1,
                int(match.group(2)),
                problem.id,
            )
    return (2, problem.id)


@router.get("/problems", response_model=list[ProblemOut])
def list_problems(
    q: str = Query(default="", max_length=100),
    difficulty: str = Query(default=""),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Problem]:
    query = db.query(Problem)
    if q:
        query = query.filter(Problem.title.contains(q))
    if difficulty in {"easy", "medium", "hard"}:
        query = query.filter(Problem.difficulty == difficulty)
    problems = query.order_by(Problem.id).all()
    return sorted(problems, key=_teaching_rank)


@router.post("/problems", response_model=ProblemDetail, status_code=status.HTTP_201_CREATED)
def create_problem(
    payload: ProblemCreate,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> Problem:
    problem = Problem(
        title=payload.title,
        description=payload.description,
        language=payload.language,
        starter_code=payload.starter_code,
        difficulty=payload.difficulty,
        tags=payload.tags,
        created_by=teacher.id,
    )
    db.add(problem)
    db.flush()
    for case in payload.test_cases:
        db.add(
            TestCase(
                problem_id=problem.id,
                input=case.input,
                expected_output=case.expected_output,
                is_sample=case.is_sample,
            )
        )
    db.commit()
    db.refresh(problem)
    problem.starter_code = get_starter_code(problem)
    return problem


@router.post("/problems/import", response_model=ProblemImportResult)
def import_problems(
    payload: list[ProblemCreate],
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ProblemImportResult:
    created = 0
    updated = 0

    for item in payload:
        problem = (
            db.query(Problem)
            .filter(
                Problem.title == item.title,
                Problem.language == item.language,
            )
            .first()
        )
        if problem:
            problem.title = item.title
            problem.description = item.description
            problem.language = item.language
            problem.starter_code = item.starter_code
            problem.difficulty = item.difficulty
            problem.tags = item.tags
            for case in list(problem.test_cases):
                db.delete(case)
            db.flush()
            updated += 1
        else:
            problem = Problem(
                title=item.title,
                description=item.description,
                language=item.language,
                starter_code=item.starter_code,
                difficulty=item.difficulty,
                tags=item.tags,
                created_by=_.id,
            )
            db.add(problem)
            db.flush()
            created += 1

        for case in item.test_cases:
            db.add(
                TestCase(
                    problem_id=problem.id,
                    input=case.input,
                    expected_output=case.expected_output,
                    is_sample=case.is_sample,
                )
            )

    db.commit()
    return ProblemImportResult(
        created=created,
        updated=updated,
        total=len(payload),
    )


@router.get("/problems/{problem_id}", response_model=ProblemDetail)
def get_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Problem:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    problem.starter_code = get_starter_code(problem)
    return problem


@router.put("/problems/{problem_id}", response_model=ProblemDetail)
def update_problem(
    problem_id: int,
    payload: ProblemUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> Problem:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    for field in ("title", "description", "language", "starter_code", "difficulty", "tags"):
        value = getattr(payload, field)
        if value is not None:
            setattr(problem, field, value)
    if payload.test_cases is not None:
        for case in list(problem.test_cases):
            db.delete(case)
        db.flush()
        for case in payload.test_cases:
            db.add(
                TestCase(
                    problem_id=problem.id,
                    input=case.input,
                    expected_output=case.expected_output,
                    is_sample=case.is_sample,
                )
            )
    db.commit()
    db.refresh(problem)
    problem.starter_code = get_starter_code(problem)
    return problem


@router.delete("/problems/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> None:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    db.query(CodeDraft).filter(CodeDraft.problem_id == problem_id).delete(
        synchronize_session=False
    )
    submission_ids = [
        submission_id
        for (submission_id,) in db.query(Submission.id)
        .filter(Submission.problem_id == problem_id)
        .all()
    ]
    if submission_ids:
        db.query(Feedback).filter(
            Feedback.submission_id.in_(submission_ids)
        ).delete(synchronize_session=False)
        db.query(Submission).filter(
            Submission.id.in_(submission_ids)
        ).delete(synchronize_session=False)
    db.delete(problem)
    db.commit()
