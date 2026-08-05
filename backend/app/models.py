from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    avatar = Column(String(500), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)


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
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False, default="python")
    status = Column(String(20), nullable=False, default="pending")
    execution_time = Column(Float, nullable=True)
    actual_output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    score = Column(Float, nullable=True)
    provider = Column(String(20), nullable=False, default="local")
    created_at = Column(DateTime, default=datetime.utcnow)
