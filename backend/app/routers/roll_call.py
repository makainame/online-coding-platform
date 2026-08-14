from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import RollCallStudent, User
from ..schemas import RollCallImportResult, RollCallStudentCreate, RollCallStudentOut
from ..security import require_teacher


router = APIRouter(tags=["roll-call"])


@router.get("/admin/roll-call/students", response_model=list[RollCallStudentOut])
def list_roll_call_students(
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> list[RollCallStudent]:
    return (
        db.query(RollCallStudent)
        .filter(RollCallStudent.teacher_id == teacher.id)
        .order_by(RollCallStudent.id)
        .all()
    )


@router.post(
    "/admin/roll-call/students",
    response_model=RollCallStudentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_roll_call_student(
    payload: RollCallStudentCreate,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> RollCallStudent:
    name = payload.name.strip()
    class_name = payload.class_name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="学生姓名不能为空")
    existing = (
        db.query(RollCallStudent)
        .filter(
            RollCallStudent.teacher_id == teacher.id,
            RollCallStudent.name == name,
            RollCallStudent.class_name == class_name,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="该班级中已存在同名学生")

    student = RollCallStudent(
        teacher_id=teacher.id,
        name=name,
        class_name=class_name,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.post(
    "/admin/roll-call/students/import",
    response_model=RollCallImportResult,
)
def import_roll_call_students(
    payload: list[RollCallStudentCreate],
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> RollCallImportResult:
    created = 0
    skipped = 0
    existing = {
        (item.name, item.class_name)
        for item in db.query(RollCallStudent)
        .filter(RollCallStudent.teacher_id == teacher.id)
        .all()
    }
    seen: set[tuple[str, str]] = set()

    for item in payload:
        name = item.name.strip()
        class_name = item.class_name.strip()
        key = (name, class_name)
        if not name or key in existing or key in seen:
            skipped += 1
            continue
        db.add(
            RollCallStudent(
                teacher_id=teacher.id,
                name=name,
                class_name=class_name,
            )
        )
        seen.add(key)
        created += 1

    db.commit()
    return RollCallImportResult(
        created=created,
        skipped=skipped,
        total=len(payload),
    )


@router.delete(
    "/admin/roll-call/students",
    status_code=status.HTTP_204_NO_CONTENT,
)
def clear_roll_call_students(
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> None:
    db.query(RollCallStudent).filter(
        RollCallStudent.teacher_id == teacher.id
    ).delete(synchronize_session=False)
    db.commit()


@router.delete(
    "/admin/roll-call/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_roll_call_student(
    student_id: int,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> None:
    student = (
        db.query(RollCallStudent)
        .filter(
            RollCallStudent.id == student_id,
            RollCallStudent.teacher_id == teacher.id,
        )
        .first()
    )
    if student is None:
        raise HTTPException(status_code=404, detail="点名学生不存在")
    db.delete(student)
    db.commit()
