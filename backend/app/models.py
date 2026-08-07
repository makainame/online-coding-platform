from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class ClassGroup(Base):
    __tablename__ = "class_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    teacher_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship(
        "User",
        back_populates="class_group",
        foreign_keys="User.class_id",
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    avatar = Column(String(500), nullable=True)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

    class_group = relationship(
        "ClassGroup",
        back_populates="students",
        foreign_keys=[class_id],
    )


class AiSetting(Base):
    __tablename__ = "ai_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    provider = Column(String(20), nullable=False, default="deepseek")
    encrypted_api_key = Column(Text, nullable=True)
    base_url = Column(String(255), nullable=True)
    model = Column(String(100), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CodeDraft(Base):
    __tablename__ = "code_drafts"
    __table_args__ = (
        UniqueConstraint("user_id", "problem_id", name="uq_user_problem_draft"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False, index=True)
    code = Column(Text, nullable=False, default="")
    language = Column(String(20), nullable=False, default="python")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    language = Column(String(20), nullable=False, default="python")
    question_type = Column(String(20), nullable=False, default="编程题")
    score = Column(Integer, nullable=True)
    starter_code = Column(Text, nullable=True)
    difficulty = Column(String(20), nullable=False, default="easy")
    tags = Column(String(200), nullable=False, default="")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    test_cases = relationship(
        "TestCase",
        cascade="all, delete-orphan",
        back_populates="problem",
        order_by="TestCase.id",
    )


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    input = Column(Text, nullable=False, default="")
    expected_output = Column(Text, nullable=False)
    is_sample = Column(Boolean, nullable=False, default=True)

    problem = relationship("Problem", back_populates="test_cases")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False, default="python")
    status = Column(String(20), nullable=False, default="pending")
    execution_time = Column(Float, nullable=True)
    actual_output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False, default="")
    duration_minutes = Column(Integer, nullable=False, default=60)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True, index=True)
    status = Column(String(20), nullable=False, default="draft")
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    problems = relationship(
        "ExamProblem",
        cascade="all, delete-orphan",
        back_populates="exam",
        order_by="ExamProblem.order_index",
    )
    attempts = relationship(
        "ExamAttempt",
        cascade="all, delete-orphan",
        back_populates="exam",
    )


class ExamProblem(Base):
    __tablename__ = "exam_problems"
    __table_args__ = (
        UniqueConstraint("exam_id", "problem_id", name="uq_exam_problem"),
    )

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    order_index = Column(Integer, nullable=False, default=0)
    score = Column(Integer, nullable=True)

    exam = relationship("Exam", back_populates="problems")
    problem = relationship("Problem")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    __table_args__ = (
        UniqueConstraint("exam_id", "user_id", name="uq_exam_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="in_progress")
    score = Column(Integer, nullable=True)
    total_problems = Column(Integer, nullable=False, default=0)
    accepted_problems = Column(Integer, nullable=False, default=0)
    paste_count = Column(Integer, nullable=False, default=0)
    switch_count = Column(Integer, nullable=False, default=0)

    exam = relationship("Exam", back_populates="attempts")
    user = relationship("User")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    score = Column(Float, nullable=True)
    provider = Column(String(20), nullable=False, default="local")
    created_at = Column(DateTime, default=datetime.utcnow)
