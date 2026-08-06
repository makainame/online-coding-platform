from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ClassGroup, Submission, User
from ..schemas import (
    ClassGroupCreate,
    ClassGroupOut,
    ClassGroupUpdate,
    StudentClassUpdate,
    StudentOut,
)
from ..security import require_teacher


router = APIRouter(tags=["classes"])


def _fill_student(db: Session, student: User) -> None:
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
    if student.class_id:
        class_group = (
            db.query(ClassGroup)
            .filter(ClassGroup.id == student.class_id)
            .first()
        )
        student.class_name = class_group.name if class_group else ""
    else:
        student.class_name = ""


@router.get("/admin/classes", response_model=list[ClassGroupOut])
def list_classes(
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> list[ClassGroup]:
    classes = db.query(ClassGroup).order_by(ClassGroup.id).all()
    if not classes:
        return classes

    class_ids = [class_group.id for class_group in classes]
    counts = dict(
        db.query(User.class_id, func.count(User.id))
        .filter(
            User.role == "student",
            User.class_id.in_(class_ids),
        )
        .group_by(User.class_id)
        .all()
    )
    for class_group in classes:
        class_group.student_count = counts.get(class_group.id, 0)
    return classes


@router.post(
    "/admin/classes",
    response_model=ClassGroupOut,
    status_code=status.HTTP_201_CREATED,
)
def create_class(
    payload: ClassGroupCreate,
    db: Session = Depends(get_db),
    teacher: User = Depends(require_teacher),
) -> ClassGroup:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="班级名称不能为空")
    existing = db.query(ClassGroup).filter(ClassGroup.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="班级名称已存在")

    class_group = ClassGroup(name=name, teacher_id=teacher.id)
    db.add(class_group)
    db.commit()
    db.refresh(class_group)
    class_group.student_count = 0
    return class_group


@router.put("/admin/classes/{class_id}", response_model=ClassGroupOut)
def update_class(
    class_id: int,
    payload: ClassGroupUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> ClassGroup:
    class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
    if class_group is None:
        raise HTTPException(status_code=404, detail="班级不存在")
    if payload.name is not None:
        new_name = payload.name.strip()
        if not new_name:
            raise HTTPException(status_code=400, detail="班级名称不能为空")
        duplicate = (
            db.query(ClassGroup)
            .filter(
                ClassGroup.name == new_name,
                ClassGroup.id != class_id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=400, detail="班级名称已存在")
        class_group.name = new_name

    db.commit()
    db.refresh(class_group)
    class_group.student_count = (
        db.query(func.count(User.id))
        .filter(
            User.role == "student",
            User.class_id == class_group.id,
        )
        .scalar()
        or 0
    )
    return class_group


@router.delete("/admin/classes/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_teacher),
) -> None:
    class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
    if class_group is None:
        raise HTTPException(status_code=404, detail="班级不存在")
    db.query(User).filter(User.class_id == class_id).update(
        {User.class_id: None},
        synchronize_session=False,
    )
    db.delete(class_group)
    db.commit()


@router.put("/admin/students/{student_id}/class", response_model=StudentOut)
def update_student_class(
    student_id: int,
    payload: StudentClassUpdate,
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

    if payload.class_id is not None:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == payload.class_id).first()
        if class_group is None:
            raise HTTPException(status_code=404, detail="班级不存在")

    student.class_id = payload.class_id
    db.commit()
    db.refresh(student)
    _fill_student(db, student)
    return student
