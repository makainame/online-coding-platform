from datetime import datetime
import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..exam_stages import EXAM_STAGES, select_stage_problem_ids
from ..models import (
    ClassGroup,
    Exam,
    ExamAttempt,
    ExamProblem,
    Problem,
    Submission,
    User,
)
from ..schemas import (
    ExamAutoCreate,
    ExamAutoPreviewOut,
    ExamAutoUpdate,
    ExamCreate,
    ExamDetail,
    ExamOut,
    ExamProblemOut,
    ExamResultOut,
    ExamStageCreate,
    ExamStartOut,
    ExamSubmitOut,
    ExamUpdate,
    ExamProblemTestCase,
    StudentExamDetail,
    StudentExamOut,
)
from ..security import get_current_user, require_teacher


router = APIRouter(tags=["exams"])


def _validate_exam_title(title: str) -> str:
    stripped = title.strip()
    if len(stripped) < 2 or not any(char.isalpha() for char in stripped):
        raise HTTPException(
            status_code=400,
            detail="考试标题不能是纯数字或太短，请填写有意义的名称",
        )
    return stripped


def _distribute_stage_scores(problems: list[Problem]) -> list[int]:
    base_score = {
        "easy": 8,
        "medium": 10,
        "hard": 12,
    }
    raw_scores = [
        base_score.get(problem.difficulty, 10)
        for problem in problems
    ]
    total_raw = sum(raw_scores) or 1
    scores = [round(100 * score / total_raw) for score in raw_scores]
    difference = 100 - sum(scores)
    if scores:
        scores[0] += difference
    return scores


def _class_name_map(db: Session, class_ids: set[int]) -> dict[int, str]:
    if not class_ids:
        return {}
    return {
        class_group.id: class_group.name
        for class_group in db.query(ClassGroup)
        .filter(ClassGroup.id.in_(class_ids))
        .all()
    }


def _select_auto_problem_ids(
    db: Session,
    knowledge_points: list[str],
    count_per_point: int,
    difficulty: str,
    language: str,
) -> list[int]:
    problems = db.query(Problem).filter(Problem.language == language).all()
    point_set = {point.strip() for point in knowledge_points if point.strip()}
    selected_ids: list[int] = []
    seen: set[int] = set()
    for point in point_set:
        candidates = []
        for problem in problems:
            tags = {tag.strip() for tag in problem.tags.split(",")}
            if point not in tags:
                continue
            if difficulty != "all" and problem.difficulty != difficulty:
                continue
            if problem.id in seen:
                continue
            candidates.append(problem)
        random.shuffle(candidates)
        chosen = candidates[:count_per_point]
        selected_ids.extend(problem.id for problem in chosen)
        seen.update(problem.id for problem in chosen)
    return selected_ids


def _attach_exam_meta(db: Session, exams: list[Exam]) -> None:
    if not exams:
        return
    exam_ids = [exam.id for exam in exams]
    class_ids = {exam.class_id for exam in exams if exam.class_id}
    class_names = _class_name_map(db, class_ids)
    problem_counts = dict(
        db.query(ExamProblem.exam_id, func.count(ExamProblem.id))
        .filter(ExamProblem.exam_id.in_(exam_ids))
        .group_by(ExamProblem.exam_id)
        .all()
    )
    attempt_counts = dict(
        db.query(ExamAttempt.exam_id, func.count(ExamAttempt.id))
        .filter(ExamAttempt.exam_id.in_(exam_ids))
        .group_by(ExamAttempt.exam_id)
        .all()
    )
    for exam in exams:
        exam.class_name = class_names.get(exam.class_id, "")
        exam.problem_count = problem_counts.get(exam.id, 0)
        exam.attempt_count = attempt_counts.get(exam.id, 0)


def _exam_description(problem: Problem) -> str:
    text = (problem.description or "").strip()
    if "示例" in text:
        return text
    samples = [
        case for case in problem.test_cases if case.is_sample
    ][:3] or problem.test_cases[:3]
    if not samples:
        return text

    lines = [text, ""]
    for index, case in enumerate(samples, start=1):
        lines.append(f"示例 {index}：")
        lines.append("输入：")
        lines.append(case.input if case.input else "（无输入）")
        lines.append("输出：")
        lines.append(case.expected_output)
        lines.append("")
    return "\n".join(lines).rstrip()


def _exam_problem_out(
    problem_link: ExamProblem,
    include_test_cases: bool = True,
) -> ExamProblemOut:
    problem = problem_link.problem
    sample_cases = [
        case for case in problem.test_cases if case.is_sample
    ]
    return ExamProblemOut(
        id=problem_link.id,
        problem_id=problem.id,
        title=problem.title,
        description=_exam_description(problem),
        language=problem.language,
        question_type=problem.question_type,
        score=problem_link.score or problem.score,
        difficulty=problem.difficulty,
        tags=problem.tags,
        order_index=problem_link.order_index,
        starter_code=_exam_starter_code(problem),
        test_cases=[
            ExamProblemTestCase(
                id=case.id,
                input=case.input,
                expected_output=case.expected_output,
                is_sample=case.is_sample,
            )
            for case in (sample_cases if include_test_cases else [])
        ],
    )


def _exam_starter_code(problem: Problem) -> str:
    if problem.language == "python":
        return "# 请根据题目要求完成代码\n"
    if problem.language == "javascript":
        return "// 请根据题目要求完成代码\n"
    if problem.language == "java":
        return (
            "public class Main {\n"
            "    public static void main(String[] args) {\n"
            "        // 请根据题目要求完成代码\n"
            "    }\n"
            "}\n"
        )
    if problem.language == "cpp":
        return (
            "#include <iostream>\n"
            "\n"
            "int main() {\n"
            "    // 请根据题目要求完成代码\n"
            "    return 0;\n"
            "}\n"
        )
    return ""


def _exam_detail(
    db: Session,
    exam: Exam,
    include_test_cases: bool = True,
) -> ExamDetail:
    _attach_exam_meta(db, [exam])
    return ExamDetail(
        id=exam.id,
        title=exam.title,
        description=exam.description,
        duration_minutes=exam.duration_minutes,
        class_id=exam.class_id,
        class_name=exam.class_name,
        status=exam.status,
        created_at=exam.created_at,
        problem_count=exam.problem_count,
        attempt_count=exam.attempt_count,
        problems=[
            _exam_problem_out(problem_link, include_test_cases)
            for problem_link in sorted(exam.problems, key=lambda item: item.order_index)
        ],
    )


def _can_access_exam(db: Session, exam: Exam, user: User) -> bool:
    if exam.class_id is not None and user.class_id != exam.class_id:
        return False
    return True


def _student_exam_detail(db: Session, exam: Exam, user: User) -> StudentExamDetail:
    detail = _exam_detail(db, exam, include_test_cases=False)
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam.id, ExamAttempt.user_id == user.id)
        .first()
    )
    results: dict[str, str] = {}
    submissions = (
        db.query(Submission)
        .filter(
            Submission.exam_id == exam.id,
            Submission.user_id == user.id,
        )
        .all()
    )
    for problem_link in exam.problems:
        problem_submissions = [
            item for item in submissions if item.problem_id == problem_link.problem_id
        ]
        if any(item.status == "accepted" for item in problem_submissions):
            results[str(problem_link.problem_id)] = "accepted"
        elif problem_submissions:
            results[str(problem_link.problem_id)] = "submitted"
        else:
            results[str(problem_link.problem_id)] = ""

    return StudentExamDetail(
        **detail.model_dump(),
        attempt_status=attempt.status if attempt else "",
        score=attempt.score if attempt else None,
        accepted_problems=attempt.accepted_problems if attempt else 0,
        total_problems=attempt.total_problems if attempt else 0,
        started_at=attempt.started_at if attempt else None,
        submitted_at=attempt.submitted_at if attempt else None,
        results=results,
    )


@router.get("/admin/exams", response_model=list[ExamOut])
def list_admin_exams(
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> list[Exam]:
    exams = db.query(Exam).order_by(Exam.id.desc()).all()
    _attach_exam_meta(db, exams)
    return exams


@router.post(
    "/admin/exams",
    response_model=ExamDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_exam(
    payload: ExamCreate,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> ExamDetail:
    title = _validate_exam_title(payload.title)
    if payload.class_id is not None:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == payload.class_id).first()
        if class_group is None:
            raise HTTPException(status_code=404, detail="班级不存在")
    problem_ids = list(dict.fromkeys(payload.problem_ids))
    if problem_ids:
        existing_problem_ids = {
            problem.id
            for problem in db.query(Problem)
            .filter(Problem.id.in_(problem_ids))
            .all()
        }
        missing = set(problem_ids) - existing_problem_ids
        if missing:
            raise HTTPException(status_code=400, detail="包含不存在的题目")

    exam = Exam(
        title=title,
        description=payload.description,
        duration_minutes=payload.duration_minutes,
        class_id=payload.class_id,
        status=payload.status,
        created_by=teacher.id,
    )
    db.add(exam)
    db.flush()
    for index, problem_id in enumerate(problem_ids):
        db.add(
            ExamProblem(
                exam_id=exam.id,
                problem_id=problem_id,
                order_index=index,
            )
        )
    db.commit()
    db.refresh(exam)
    return _exam_detail(db, exam)


@router.post(
    "/admin/exams/auto",
    response_model=ExamDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_exam_auto(
    payload: ExamAutoCreate,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> ExamDetail:
    knowledge_points = [point.strip() for point in payload.knowledge_points if point.strip()]
    if not knowledge_points:
        raise HTTPException(status_code=400, detail="请至少选择一个知识点")
    problem_ids = _select_auto_problem_ids(
        db,
        knowledge_points,
        payload.count_per_point,
        payload.difficulty,
        payload.language,
    )
    if not problem_ids:
        raise HTTPException(status_code=400, detail="没有匹配的题目，请调整知识点或难度")

    exam = Exam(
        title=_validate_exam_title(payload.title),
        description=payload.description,
        duration_minutes=payload.duration_minutes,
        class_id=payload.class_id,
        status=payload.status,
        created_by=teacher.id,
    )
    db.add(exam)
    db.flush()
    for index, problem_id in enumerate(problem_ids):
        db.add(
            ExamProblem(
                exam_id=exam.id,
                problem_id=problem_id,
                order_index=index,
            )
        )
    db.commit()
    db.refresh(exam)
    return _exam_detail(db, exam)


@router.post(
    "/admin/exams/stage",
    response_model=ExamDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_stage_exam(
    payload: ExamStageCreate,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> ExamDetail:
    if payload.stage not in EXAM_STAGES:
        raise HTTPException(status_code=400, detail="阶段模板不存在")
    if payload.language != "python":
        raise HTTPException(status_code=400, detail="阶段卷暂只支持 Python 题库")

    problem_ids = select_stage_problem_ids(
        db,
        payload.stage,
        language=payload.language,
        target_count=payload.target_count,
    )
    if not problem_ids:
        raise HTTPException(status_code=400, detail="当前阶段没有可组卷题目")
    if payload.class_id is not None:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == payload.class_id).first()
        if class_group is None:
            raise HTTPException(status_code=404, detail="班级不存在")

    problem_by_id = {
        problem.id: problem
        for problem in db.query(Problem)
        .filter(Problem.id.in_(problem_ids))
        .all()
    }
    stage_problems = [problem_by_id[problem_id] for problem_id in problem_ids]
    stage_scores = _distribute_stage_scores(stage_problems)

    title = (
        _validate_exam_title(payload.title)
        if payload.title and payload.title.strip()
        else EXAM_STAGES[payload.stage]["title"]
    )
    exam = Exam(
        title=title,
        description=payload.description,
        duration_minutes=payload.duration_minutes,
        class_id=payload.class_id,
        status=payload.status,
        created_by=teacher.id,
    )
    db.add(exam)
    db.flush()
    for index, (problem_id, score) in enumerate(zip(problem_ids, stage_scores)):
        db.add(
            ExamProblem(
                exam_id=exam.id,
                problem_id=problem_id,
                order_index=index,
                score=score,
            )
        )
    db.commit()
    db.refresh(exam)
    return _exam_detail(db, exam)


@router.post("/admin/exams/preview", response_model=ExamAutoPreviewOut)
def preview_exam_auto_select(
    payload: ExamAutoUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ExamAutoPreviewOut:
    knowledge_points = [point.strip() for point in payload.knowledge_points if point.strip()]
    if not knowledge_points:
        raise HTTPException(status_code=400, detail="请至少选择一个知识点")
    problem_ids = _select_auto_problem_ids(
        db,
        knowledge_points,
        payload.count_per_point,
        payload.difficulty,
        payload.language,
    )
    if not problem_ids:
        raise HTTPException(status_code=400, detail="没有匹配的题目，请调整知识点或难度")
    return ExamAutoPreviewOut(problem_ids=problem_ids)


@router.get("/admin/exams/{exam_id}", response_model=ExamDetail)
def get_admin_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ExamDetail:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    return _exam_detail(db, exam)


@router.put("/admin/exams/{exam_id}", response_model=ExamDetail)
def update_exam(
    exam_id: int,
    payload: ExamUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ExamDetail:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")

    if payload.title is not None:
        exam.title = _validate_exam_title(payload.title)
    if payload.description is not None:
        exam.description = payload.description
    if payload.duration_minutes is not None:
        exam.duration_minutes = payload.duration_minutes
    if payload.class_id is not None:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == payload.class_id).first()
        if class_group is None:
            raise HTTPException(status_code=404, detail="班级不存在")
        exam.class_id = payload.class_id
    if payload.status is not None:
        exam.status = payload.status

    if payload.problem_ids is not None:
        problem_ids = list(dict.fromkeys(payload.problem_ids))
        if problem_ids:
            existing_problem_ids = {
                problem.id
                for problem in db.query(Problem)
                .filter(Problem.id.in_(problem_ids))
                .all()
            }
            missing = set(problem_ids) - existing_problem_ids
            if missing:
                raise HTTPException(status_code=400, detail="包含不存在的题目")
        for problem_link in list(exam.problems):
            db.delete(problem_link)
        db.flush()
        for index, problem_id in enumerate(problem_ids):
            db.add(
                ExamProblem(
                    exam_id=exam.id,
                    problem_id=problem_id,
                    order_index=index,
                )
            )

    db.commit()
    db.refresh(exam)
    return _exam_detail(db, exam)


@router.put("/admin/exams/{exam_id}/auto-select", response_model=ExamDetail)
def update_exam_auto_select(
    exam_id: int,
    payload: ExamAutoUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ExamDetail:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    knowledge_points = [point.strip() for point in payload.knowledge_points if point.strip()]
    if not knowledge_points:
        raise HTTPException(status_code=400, detail="请至少选择一个知识点")
    problem_ids = _select_auto_problem_ids(
        db,
        knowledge_points,
        payload.count_per_point,
        payload.difficulty,
        payload.language,
    )
    if not problem_ids:
        raise HTTPException(status_code=400, detail="没有匹配的题目，请调整知识点或难度")

    for problem_link in list(exam.problems):
        db.delete(problem_link)
    db.flush()
    for index, problem_id in enumerate(problem_ids):
        db.add(
            ExamProblem(
                exam_id=exam.id,
                problem_id=problem_id,
                order_index=index,
            )
        )
    db.commit()
    db.refresh(exam)
    return _exam_detail(db, exam)


@router.delete("/admin/exams/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> None:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    db.query(Submission).filter(Submission.exam_id == exam_id).update(
        {Submission.exam_id: None},
        synchronize_session=False,
    )
    db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id).delete(
        synchronize_session=False,
    )
    db.query(ExamProblem).filter(ExamProblem.exam_id == exam_id).delete(
        synchronize_session=False,
    )
    db.delete(exam)
    db.commit()


@router.get("/admin/exams/{exam_id}/results", response_model=list[ExamResultOut])
def get_exam_results(
    exam_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> list[ExamResultOut]:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    attempts = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam_id)
        .order_by(ExamAttempt.id)
        .all()
    )
    users = {
        user.id: user
        for user in db.query(User)
        .filter(User.id.in_([attempt.user_id for attempt in attempts]))
        .all()
    }
    class_names = _class_name_map(
        db,
        {user.class_id for user in users.values() if user.class_id},
    )
    submissions = (
        db.query(Submission)
        .filter(Submission.exam_id == exam_id)
        .all()
    )
    status_by_user_problem: dict[int, dict[int, str]] = {}
    for submission in submissions:
        user_map = status_by_user_problem.setdefault(submission.user_id, {})
        if submission.status == "accepted":
            user_map[submission.problem_id] = "accepted"
        elif submission.problem_id not in user_map:
            user_map[submission.problem_id] = "submitted"
    problem_links = exam.problems
    return [
        ExamResultOut(
            user_id=attempt.user_id,
            username=users[attempt.user_id].username,
            email=users[attempt.user_id].email,
            class_name=class_names.get(users[attempt.user_id].class_id, ""),
            status=attempt.status,
            score=attempt.score,
            total_problems=attempt.total_problems,
            accepted_problems=attempt.accepted_problems,
            started_at=attempt.started_at,
            submitted_at=attempt.submitted_at,
            problem_statuses={
                str(problem_link.problem_id): status_by_user_problem.get(
                    attempt.user_id,
                    {},
                ).get(problem_link.problem_id, "")
                for problem_link in problem_links
            },
        )
        for attempt in attempts
    ]


@router.get("/admin/exams/{exam_id}/results/export", response_model=list[ExamResultOut])
def export_exam_results(
    exam_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> list[ExamResultOut]:
    return get_exam_results(exam_id, db, _)


@router.get("/exams", response_model=list[StudentExamOut])
def list_student_exams(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[StudentExamOut]:
    attempts = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.user_id == user.id)
        .all()
    )
    attempt_by_exam = {attempt.exam_id: attempt for attempt in attempts}
    published_query = db.query(Exam).filter(Exam.status == "published")
    if user.class_id is not None:
        published_query = published_query.filter(
            or_(Exam.class_id.is_(None), Exam.class_id == user.class_id)
        )
    else:
        published_query = published_query.filter(Exam.class_id.is_(None))

    closed_ids = [
        attempt.exam_id
        for attempt in attempts
        if attempt.exam_id in attempt_by_exam
    ]
    exams = published_query.order_by(Exam.id.desc()).all()
    if closed_ids:
        closed_exams = (
            db.query(Exam)
            .filter(
                Exam.id.in_(closed_ids),
                Exam.status == "closed",
            )
            .all()
        )
        existing_ids = {exam.id for exam in exams}
        exams.extend(exam for exam in closed_exams if exam.id not in existing_ids)

    class_names = _class_name_map(
        db,
        {exam.class_id for exam in exams if exam.class_id},
    )
    result = []
    for exam in exams:
        attempt = attempt_by_exam.get(exam.id)
        result.append(
            StudentExamOut(
                id=exam.id,
                title=exam.title,
                description=exam.description,
                duration_minutes=exam.duration_minutes,
                class_name=class_names.get(exam.class_id, ""),
                status=exam.status,
                attempt_status=attempt.status if attempt else "",
                score=attempt.score if attempt else None,
                accepted_problems=attempt.accepted_problems if attempt else 0,
                total_problems=attempt.total_problems if attempt else 0,
            )
        )
    return result


@router.get("/exams/{exam_id}", response_model=StudentExamDetail)
def get_student_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> StudentExamDetail:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam.id, ExamAttempt.user_id == user.id)
        .first()
    )
    if exam.status == "published":
        if not _can_access_exam(db, exam, user):
            raise HTTPException(status_code=403, detail="无权参加该考试")
    elif attempt is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    return _student_exam_detail(db, exam, user)


@router.post("/exams/{exam_id}/start", response_model=ExamStartOut)
def start_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ExamStartOut:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None or exam.status != "published":
        raise HTTPException(status_code=404, detail="考试不存在或未发布")
    if not _can_access_exam(db, exam, user):
        raise HTTPException(status_code=403, detail="无权参加该考试")

    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam.id, ExamAttempt.user_id == user.id)
        .first()
    )
    if attempt is not None:
        if attempt.status == "submitted":
            raise HTTPException(status_code=400, detail="考试已提交")
        return ExamStartOut(
            attempt_id=attempt.id,
            status=attempt.status,
            started_at=attempt.started_at,
        )

    total_problems = (
        db.query(func.count(ExamProblem.id))
        .filter(ExamProblem.exam_id == exam.id)
        .scalar()
        or 0
    )
    attempt = ExamAttempt(
        exam_id=exam.id,
        user_id=user.id,
        total_problems=total_problems,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return ExamStartOut(
        attempt_id=attempt.id,
        status=attempt.status,
        started_at=attempt.started_at,
    )


@router.post("/exams/{exam_id}/submit", response_model=ExamSubmitOut)
def submit_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ExamSubmitOut:
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="考试不存在")
    attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.exam_id == exam.id, ExamAttempt.user_id == user.id)
        .first()
    )
    if attempt is None:
        raise HTTPException(status_code=400, detail="请先开始考试")
    if attempt.status == "submitted":
        return ExamSubmitOut(
            status=attempt.status,
            score=attempt.score or 0,
            total_problems=attempt.total_problems,
            accepted_problems=attempt.accepted_problems,
            submitted_at=attempt.submitted_at,
        )

    submissions = (
        db.query(Submission)
        .filter(
            Submission.exam_id == exam.id,
            Submission.user_id == user.id,
        )
        .all()
    )
    accepted_problem_ids = {
        submission.problem_id
        for submission in submissions
        if submission.status == "accepted"
    }
    problem_count = len(exam.problems)
    accepted_problems = len(accepted_problem_ids)
    total_score = sum(
        problem_link.score or problem_link.problem.score or 1
        for problem_link in exam.problems
    )
    accepted_score = sum(
        problem_link.score or problem_link.problem.score or 1
        for problem_link in exam.problems
        if problem_link.problem_id in accepted_problem_ids
    )
    attempt.status = "submitted"
    attempt.submitted_at = datetime.utcnow()
    attempt.score = round(accepted_score / total_score * 100) if total_score else 0
    attempt.accepted_problems = accepted_problems
    attempt.total_problems = problem_count
    db.commit()
    db.refresh(attempt)
    return ExamSubmitOut(
        status=attempt.status,
        score=attempt.score or 0,
        total_problems=attempt.total_problems,
        accepted_problems=attempt.accepted_problems,
        submitted_at=attempt.submitted_at,
    )
