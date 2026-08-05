import base64
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import config
from ..ai_crypto import encrypt_api_key
from ..config import BASE_DIR
from ..database import get_db
from ..models import AiSetting, User
from ..schemas import AuthResponse, LoginRequest, RegisterRequest, UserOut
from ..security import create_token, get_current_user, hash_password, verify_password


router = APIRouter(tags=["auth"])

AVATAR_DIR = BASE_DIR / "uploads" / "avatars"


def _save_avatar(avatar_base64: str | None) -> str | None:
    if not avatar_base64:
        return None
    if avatar_base64.startswith("data:image"):
        header, encoded = avatar_base64.split(",", 1)
        extension = ".png" if "png" in header.lower() else ".jpg"
    else:
        encoded = avatar_base64
        extension = ".png"
    try:
        raw = base64.b64decode(encoded)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="头像数据无效",
        ) from exc
    if len(raw) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="头像不能超过 2MB",
        )
    AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{extension}"
    (AVATAR_DIR / filename).write_bytes(raw)
    return f"/uploads/avatars/{filename}"


@router.post("/auth/register", response_model=AuthResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    if payload.role == "teacher":
        if payload.teacher_code != config.TEACHER_REGISTER_CODE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="教师授权码错误",
            )
    elif payload.role != "student":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的注册角色",
        )
    if payload.role == "student" and not payload.ai_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="学生注册时必须填写自己的 AI API Key",
        )

    conditions = [User.username == payload.username]
    if payload.email:
        conditions.append(User.email == payload.email)
    existing = db.query(User).filter(or_(*conditions)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在",
        )
    user = User(
        username=payload.username,
        email=payload.email,
        avatar=_save_avatar(payload.avatar_base64),
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()
    if payload.ai_api_key:
        db.add(
            AiSetting(
                user_id=user.id,
                provider=payload.ai_provider,
                encrypted_api_key=encrypt_api_key(payload.ai_api_key),
                base_url=payload.ai_base_url,
                model=payload.ai_model,
            )
        )
    db.commit()
    db.refresh(user)
    token = create_token(db, user)
    return AuthResponse(token=token, user=UserOut.model_validate(user))


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    token = create_token(db, user)
    return AuthResponse(token=token, user=UserOut.model_validate(user))


@router.get("/users/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)
