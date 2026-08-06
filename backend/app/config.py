import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _database_url() -> str:
    value = os.getenv("DATABASE_URL")
    if value:
        return value
    db_path = (BASE_DIR / "coding_platform.db").as_posix()
    return f"sqlite:///{db_path}"


DATABASE_URL = _database_url()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
TOKEN_TTL_DAYS = int(os.getenv("TOKEN_TTL_DAYS", "7"))
TEACHER_REGISTER_CODE = os.getenv("TEACHER_REGISTER_CODE", "teacher2026")
SEED_DEMO_ACCOUNTS = os.getenv("SEED_DEMO_ACCOUNTS", "true").lower() in {"1", "true", "yes"}

AI_PROVIDER = os.getenv("AI_PROVIDER", "local").lower()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen3.7-plus")

EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", "5"))
CPP_EXECUTION_TIMEOUT = int(os.getenv("CPP_EXECUTION_TIMEOUT", "15"))
MAX_OUTPUT_LENGTH = int(os.getenv("MAX_OUTPUT_LENGTH", "10000"))
EXECUTION_MODE = os.getenv("EXECUTION_MODE", "subprocess").lower()
PYTHON_RUNNER_IMAGE = os.getenv("PYTHON_RUNNER_IMAGE", "python:3.12-slim")
NODE_RUNNER_IMAGE = os.getenv("NODE_RUNNER_IMAGE", "node:20-alpine")
JAVA_RUNNER_IMAGE = os.getenv("JAVA_RUNNER_IMAGE", "openjdk:17-jdk-slim")
CPP_RUNNER_IMAGE = os.getenv("CPP_RUNNER_IMAGE", "gcc:13-bookworm")
