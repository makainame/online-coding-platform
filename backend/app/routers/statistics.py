from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Problem, Submission, User
from ..schemas import DailyStatOut, DifficultyStatOut, UserStatsOut
from ..security import get_current_user


router = APIRouter(tags=["statistics"])


@router.get("/statistics/me", response_model=UserStatsOut)
def my_statistics(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserStatsOut:
    submissions = (
        db.query(Submission)
        .filter(Submission.user_id == user.id)
        .all()
    )
    total = len(submissions)
    accepted_count = sum(1 for item in submissions if item.status == "accepted")
    wrong_count = sum(1 for item in submissions if item.status == "wrong_answer")
    error_count = sum(1 for item in submissions if item.status == "error")
    pass_rate = round(accepted_count / total * 100, 1) if total else 0.0

    today = datetime.utcnow().date().isoformat()
    today_count = sum(
        1
        for item in submissions
        if item.created_at and item.created_at.date().isoformat() == today
    )

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

    problem_ids = {item.problem_id for item in submissions}
    difficulty_map: dict[str, int] = {}
    if problem_ids:
        problems = (
            db.query(Problem)
            .filter(Problem.id.in_(problem_ids))
            .all()
        )
        difficulty_by_id = {problem.id: problem.difficulty for problem in problems}
        for item in submissions:
            difficulty = difficulty_by_id.get(item.problem_id, "unknown")
            difficulty_map[difficulty] = difficulty_map.get(difficulty, 0) + 1

    by_difficulty = [
        DifficultyStatOut(difficulty=difficulty, submissions=count)
        for difficulty, count in sorted(difficulty_map.items())
    ]

    return UserStatsOut(
        total_submissions=total,
        accepted_count=accepted_count,
        wrong_count=wrong_count,
        error_count=error_count,
        pass_rate=pass_rate,
        today_count=today_count,
        daily=daily,
        by_difficulty=by_difficulty,
    )
