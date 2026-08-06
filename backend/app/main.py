from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from . import models  # noqa: F401
from .config import BASE_DIR
from .database import Base, engine, get_db
from .routers import ai_settings, auth, classes, drafts, exams, feedback, problems, statistics, students, submissions
from .seed import seed_data


UPLOAD_DIR = BASE_DIR / "uploads" / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if "problems" in inspector.get_table_names():
        columns = [column["name"] for column in inspector.get_columns("problems")]
        if "language" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE problems "
                        "ADD COLUMN language VARCHAR(20) NOT NULL DEFAULT 'python'"
                    )
                )
        if "starter_code" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE problems "
                        "ADD COLUMN starter_code TEXT"
                    )
                )
        if "question_type" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE problems "
                        "ADD COLUMN question_type VARCHAR(20) NOT NULL DEFAULT '编程题'"
                    )
                )
        if "score" not in columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE problems "
                        "ADD COLUMN score INTEGER"
                    )
                )
    if "users" in inspector.get_table_names():
        user_columns = [column["name"] for column in inspector.get_columns("users")]
        if "avatar" not in user_columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN avatar VARCHAR(500)"
                    )
                )
        if "class_id" not in user_columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN class_id INTEGER"
                    )
                )
    if "submissions" in inspector.get_table_names():
        submission_columns = [
            column["name"] for column in inspector.get_columns("submissions")
        ]
        if "exam_id" not in submission_columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE submissions "
                        "ADD COLUMN exam_id INTEGER"
                    )
                )
    if "exams" in inspector.get_table_names():
        exam_columns = [column["name"] for column in inspector.get_columns("exams")]
        if "class_id" not in exam_columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE exams "
                        "ADD COLUMN class_id INTEGER"
                    )
                )
    if "exam_problems" in inspector.get_table_names():
        exam_problem_columns = [
            column["name"] for column in inspector.get_columns("exam_problems")
        ]
        if "score" not in exam_problem_columns:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE exam_problems "
                        "ADD COLUMN score INTEGER"
                    )
                )


ensure_schema()

app = FastAPI(
    title="在线代码练习平台 API",
    description="AI 辅助开发的在线代码练习平台 MVP",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(problems.router, prefix="/api")
app.include_router(submissions.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(statistics.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(classes.router, prefix="/api")
app.include_router(exams.router, prefix="/api")
app.include_router(ai_settings.router, prefix="/api")
app.include_router(drafts.router, prefix="/api")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.on_event("startup")
def startup_seed() -> None:
    db: Session = next(get_db())
    try:
        seed_data(db)
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"name": "在线代码练习平台", "docs": "/docs", "status": "running"}
