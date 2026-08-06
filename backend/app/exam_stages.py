from sqlalchemy.orm import Session

from .models import Problem


EXAM_STAGES = {
    "stage1": {
        "label": "Python 阶段一（Day01-Day03）",
        "title": "Python 阶段检测一（Day01-Day03）",
        "tags": ["Day01", "Day02", "Day03"],
    },
    "stage2": {
        "label": "Python 阶段二（Day04-Day05）",
        "title": "Python 阶段检测二（Day04-Day05）",
        "tags": ["Day04", "Day05"],
    },
    "stage3": {
        "label": "Python 阶段三（Day06-Day08）",
        "title": "Python 阶段检测三（Day06-Day08）",
        "tags": ["Day06", "Day07", "Day08"],
    },
    "advanced": {
        "label": "Python 进阶综合（进阶Day01-Day08）",
        "title": "Python 进阶阶段检测（进阶Day01-Day08）",
        "tags": [
            "进阶Day01",
            "进阶Day02",
            "进阶Day03",
            "进阶Day04",
            "进阶Day05",
            "进阶Day06",
            "进阶Day07",
            "进阶Day08",
        ],
    },
    "case": {
        "label": "Python 综合案例检测",
        "title": "Python 综合案例检测卷",
        "tags": ["案例检测"],
    },
}


DIFFICULTY_RATIO = {
    "easy": 0.6,
    "medium": 0.3,
    "hard": 0.1,
}


def distribute_equal_scores(count: int) -> list[int]:
    if count <= 0:
        return []
    base, remainder = divmod(100, count)
    return [base + 1 if index < remainder else base for index in range(count)]


def _tag_set(problem: Problem) -> set[str]:
    return {tag.strip() for tag in problem.tags.split(",") if tag.strip()}


def select_stage_problem_ids(
    db: Session,
    stage: str,
    language: str = "python",
    target_count: int = 10,
) -> list[int]:
    stage_config = EXAM_STAGES[stage]
    stage_tags = stage_config["tags"]
    tag_order = {tag: index for index, tag in enumerate(stage_tags)}

    problems = (
        db.query(Problem)
        .filter(Problem.language == language)
        .all()
    )
    problems = [
        problem
        for problem in problems
        if tag_order.keys() & _tag_set(problem)
    ]
    if not problems:
        return []

    by_id = {problem.id: problem for problem in problems}
    selected: list[int] = []
    seen: set[int] = set()

    # 先保证阶段内每个知识点至少覆盖 1 题。
    for tag in stage_tags:
        candidates = [
            problem
            for problem in problems
            if tag in _tag_set(problem) and problem.id not in seen
        ]
        if not candidates:
            continue
        preferred = [
            problem for problem in candidates if problem.difficulty == "easy"
        ]
        chosen = preferred[0] if preferred else candidates[0]
        selected.append(chosen.id)
        seen.add(chosen.id)
        if len(selected) >= target_count:
            break

    remaining = target_count - len(selected)
    if remaining > 0:
        pools = {
            difficulty: [
                problem.id
                for problem in problems
                if problem.difficulty == difficulty and problem.id not in seen
            ]
            for difficulty in ("easy", "medium", "hard")
        }
        desired = {
            difficulty: round(target_count * ratio)
            for difficulty, ratio in DIFFICULTY_RATIO.items()
        }

        for difficulty in ("easy", "medium", "hard"):
            while (
                desired[difficulty]
                > sum(
                    by_id[problem_id].difficulty == difficulty
                    for problem_id in selected
                )
                and pools[difficulty]
                and len(selected) < target_count
            ):
                problem_id = pools[difficulty].pop(0)
                selected.append(problem_id)
                seen.add(problem_id)

        for difficulty in ("easy", "medium", "hard"):
            while pools[difficulty] and len(selected) < target_count:
                problem_id = pools[difficulty].pop(0)
                selected.append(problem_id)
                seen.add(problem_id)

    selected_problems = [by_id[problem_id] for problem_id in selected]
    selected_problems.sort(
        key=lambda problem: (
            min(tag_order[tag] for tag in stage_tags if tag in _tag_set(problem)),
            {"easy": 0, "medium": 1, "hard": 2}.get(problem.difficulty, 3),
            problem.id,
        )
    )
    return [problem.id for problem in selected_problems]
