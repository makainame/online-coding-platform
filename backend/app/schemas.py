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
    class_id: Optional[int] = None
    class_name: str = ""
    created_at: object


class AdminStudentStatOut(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    class_id: Optional[int] = None
    class_name: str = ""
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


class ScoreExportProblem(BaseModel):
    problem_id: int
    title: str
    language: str


class StudentScoreExportRow(BaseModel):
    username: str
    email: Optional[str] = None
    class_id: Optional[int] = None
    class_name: str = ""
    submission_count: int
    accepted_count: int
    pass_rate: float
    problem_statuses: dict[str, str]


class ScoreExportOut(BaseModel):
    problems: list[ScoreExportProblem]
    rows: list[StudentScoreExportRow]


class ClassGroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ClassGroupUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class ClassGroupOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    teacher_id: Optional[int] = None
    created_at: object
    student_count: int = 0


class StudentClassUpdate(BaseModel):
    class_id: Optional[int] = None


class ExamCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    duration_minutes: int = Field(default=60, ge=1, le=600)
    class_id: Optional[int] = None
    problem_ids: list[int] = []
    status: Literal["draft", "published", "closed"] = "draft"


class ExamUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(default=None, ge=1, le=600)
    class_id: Optional[int] = None
    problem_ids: Optional[list[int]] = None
    status: Optional[Literal["draft", "published", "closed"]] = None


class ExamAutoCreate(ExamCreate):
    knowledge_points: list[str] = []
    count_per_point: int = Field(default=3, ge=1, le=30)
    difficulty: Literal["easy", "medium", "hard", "all"] = "all"
    language: Literal["python", "javascript", "java", "cpp"] = "python"


class ExamAutoUpdate(BaseModel):
    knowledge_points: list[str] = []
    count_per_point: int = Field(default=3, ge=1, le=30)
    difficulty: Literal["easy", "medium", "hard", "all"] = "all"
    language: Literal["python", "javascript", "java", "cpp"] = "python"


class ExamAutoPreviewOut(BaseModel):
    problem_ids: list[int]


class ExamStageCreate(BaseModel):
    stage: Literal[
        "stage1",
        "stage2",
        "stage3",
        "advanced",
        "case",
    ]
    title: Optional[str] = None
    description: str = ""
    duration_minutes: int = Field(default=60, ge=1, le=600)
    class_id: Optional[int] = None
    status: Literal["draft", "published", "closed"] = "draft"
    target_count: int = Field(default=10, ge=5, le=30)
    language: str = "python"


class ExamProblemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    problem_id: int
    title: str
    language: str
    question_type: str = "编程题"
    score: Optional[int] = None
    difficulty: str
    tags: str
    order_index: int
    starter_code: Optional[str] = ""


class ExamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    duration_minutes: int
    class_id: Optional[int] = None
    class_name: str = ""
    status: str
    created_at: object
    problem_count: int = 0
    attempt_count: int = 0


class ExamDetail(ExamOut):
    problems: list[ExamProblemOut] = []


class StudentExamOut(BaseModel):
    id: int
    title: str
    description: str
    duration_minutes: int
    class_name: str = ""
    status: str
    attempt_status: str = ""
    score: Optional[int] = None
    accepted_problems: int = 0
    total_problems: int = 0


class StudentExamDetail(ExamDetail):
    attempt_status: str = ""
    score: Optional[int] = None
    accepted_problems: int = 0
    total_problems: int = 0
    started_at: object = None
    submitted_at: object = None
    results: dict[str, str] = {}


class ExamStartOut(BaseModel):
    attempt_id: int
    status: str
    started_at: object


class ExamSubmitOut(BaseModel):
    status: str
    score: int
    total_problems: int
    accepted_problems: int
    submitted_at: object


class ExamResultOut(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    class_name: str = ""
    status: str
    score: Optional[int] = None
    total_problems: int
    accepted_problems: int
    started_at: object
    submitted_at: object = None
    problem_statuses: dict[str, str] = {}


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
    question_type: str = "编程题"
    score: Optional[int] = Field(default=None, ge=1, le=100)
    starter_code: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "easy"
    tags: str = ""
    test_cases: list[TestCaseIn] = []


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    question_type: Optional[str] = None
    score: Optional[int] = Field(default=None, ge=1, le=100)
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
    question_type: str = "编程题"
    score: Optional[int] = None
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
    exam_id: Optional[int] = None


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
    exam_id: Optional[int] = None
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
