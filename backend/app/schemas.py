from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=100)
    email: Optional[str] = None
    role: Literal["student", "teacher"] = "student"
    ai_provider: Literal["deepseek", "qwen"] = "deepseek"
    ai_base_url: Optional[str] = None
    ai_model: Optional[str] = None
    ai_api_key: Optional[str] = None
    teacher_code: Optional[str] = None
    avatar_base64: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[str] = None
    avatar: Optional[str] = None
    role: str


class StudentCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=100)
    email: Optional[str] = None
    ai_provider: Literal["deepseek", "qwen"] = "deepseek"
    ai_base_url: Optional[str] = None
    ai_model: Optional[str] = None
    ai_api_key: Optional[str] = None


class StudentImportResult(BaseModel):
    created: int
    skipped: int
    total: int


class PasswordReset(BaseModel):
    password: str = Field(min_length=6, max_length=100)


class StudentOut(UserOut):
    submission_count: int = 0
    accepted_count: int = 0
    created_at: object


class AdminStudentStatOut(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    submission_count: int
    accepted_count: int
    pass_rate: float


class AdminStatsOut(BaseModel):
    total_students: int
    total_submissions: int
    accepted_count: int
    wrong_count: int
    error_count: int
    pass_rate: float
    students: list[AdminStudentStatOut]
    daily: list[DailyStatOut] = []


class AuthResponse(BaseModel):
    token: str
    user: UserOut


class TestCaseIn(BaseModel):
    input: str = ""
    expected_output: str
    is_sample: bool = True


class TestCaseOut(TestCaseIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    problem_id: int


class ProblemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str
    language: str = "python"
    starter_code: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "easy"
    tags: str = ""
    test_cases: list[TestCaseIn] = []


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    starter_code: Optional[str] = None
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None
    tags: Optional[str] = None
    test_cases: Optional[list[TestCaseIn]] = None


class ProblemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    language: str = "python"
    starter_code: Optional[str] = ""
    difficulty: str
    tags: str
    created_by: Optional[int] = None
    created_at: object


class ProblemDetail(ProblemOut):
    test_cases: list[TestCaseOut] = []


class ProblemImportResult(BaseModel):
    created: int
    updated: int
    total: int


class ExecuteRequest(BaseModel):
    problem_id: int
    code: str
    language: str = "python"
    custom_input: Optional[str] = None


class SubmissionCreate(BaseModel):
    problem_id: int
    code: str
    language: str = "python"


class TestResultOut(BaseModel):
    case_id: Optional[int] = None
    passed: bool
    input: str
    expected_output: str
    actual_output: str = ""
    error: str = ""


class ExecuteResultOut(BaseModel):
    status: str
    execution_time: float = 0
    results: list[TestResultOut] = []
    error_message: str = ""


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    code: str
    language: str
    status: str
    execution_time: Optional[float] = None
    actual_output: Optional[str] = None
    error_message: Optional[str] = None
    created_at: object


class SubmissionDetail(SubmissionOut):
    results: list[TestResultOut] = []


class FeedbackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submission_id: int
    feedback_text: str
    score: Optional[float] = None
    provider: str
    created_at: object


class DailyStatOut(BaseModel):
    date: str
    submissions: int
    accepted: int


class DifficultyStatOut(BaseModel):
    difficulty: str
    submissions: int


class UserStatsOut(BaseModel):
    total_submissions: int
    accepted_count: int
    wrong_count: int
    error_count: int
    pass_rate: float
    today_count: int
    daily: list[DailyStatOut]
    by_difficulty: list[DifficultyStatOut]


class AiSettingsOut(BaseModel):
    provider: str
    base_url: str
    model: str
    has_key: bool
    masked_key: str = ""


class AiSettingsUpdate(BaseModel):
    provider: Literal["deepseek", "qwen"] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None


class AiSettingsTestRequest(BaseModel):
    provider: Literal["deepseek", "qwen"] = "deepseek"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None


class AiSettingsTestOut(BaseModel):
    ok: bool
    message: str


class CodeDraftSave(BaseModel):
    code: str
    language: str = "python"


class CodeDraftOut(BaseModel):
    code: str = ""
    language: str = "python"
    updated_at: object = None
