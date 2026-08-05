from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import config
from ..ai_crypto import decrypt_api_key, encrypt_api_key
from ..database import get_db
from ..models import AiSetting, User
from ..schemas import (
    AiSettingsOut,
    AiSettingsTestOut,
    AiSettingsTestRequest,
    AiSettingsUpdate,
)
from ..security import get_current_user
from ..services.ai_feedback import _call_llm


router = APIRouter(tags=["ai-settings"])


def _default_provider() -> str:
    if config.AI_PROVIDER == "qwen" and config.QWEN_API_KEY:
        return "qwen"
    return "deepseek"


def _mask_key(api_key: str | None) -> str:
    if not api_key:
        return ""
    if len(api_key) <= 8:
        return "已配置"
    return f"{api_key[:4]}...{api_key[-4:]}"


def _settings_out(row: AiSetting | None, user: User) -> AiSettingsOut:
    provider = row.provider if row and row.provider else _default_provider()
    if provider == "qwen":
        base_url = (row.base_url if row and row.base_url else None) or config.QWEN_BASE_URL
        model = (row.model if row and row.model else None) or config.QWEN_MODEL
    else:
        base_url = (row.base_url if row and row.base_url else None) or config.DEEPSEEK_BASE_URL
        model = (row.model if row and row.model else None) or config.DEEPSEEK_MODEL

    has_key = bool(row and row.encrypted_api_key)
    masked_key = ""
    if has_key:
        try:
            masked_key = _mask_key(decrypt_api_key(row.encrypted_api_key))
        except ValueError:
            masked_key = "解密失败，请重新配置"
    return AiSettingsOut(
        provider=provider,
        base_url=base_url,
        model=model,
        has_key=has_key,
        masked_key=masked_key,
    )


@router.get("/ai/settings", response_model=AiSettingsOut)
def get_ai_settings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AiSettingsOut:
    row = (
        db.query(AiSetting)
        .filter(AiSetting.user_id == user.id)
        .first()
    )
    return _settings_out(row, user)


@router.put("/ai/settings", response_model=AiSettingsOut)
def update_ai_settings(
    payload: AiSettingsUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AiSettingsOut:
    row = (
        db.query(AiSetting)
        .filter(AiSetting.user_id == user.id)
        .first()
    )
    if row is None:
        row = AiSetting(user_id=user.id)
        db.add(row)

    row.provider = payload.provider
    if payload.base_url:
        row.base_url = payload.base_url
    if payload.model:
        row.model = payload.model
    if payload.api_key:
        row.encrypted_api_key = encrypt_api_key(payload.api_key)
    db.commit()
    db.refresh(row)
    return _settings_out(row, user)


@router.delete("/ai/settings", response_model=AiSettingsOut)
def delete_ai_settings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AiSettingsOut:
    row = (
        db.query(AiSetting)
        .filter(AiSetting.user_id == user.id)
        .first()
    )
    if row:
        row.encrypted_api_key = None
        db.commit()
        db.refresh(row)
    return _settings_out(row, user)


@router.post("/ai/settings/test", response_model=AiSettingsTestOut)
def test_ai_settings(
    payload: AiSettingsTestRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AiSettingsTestOut:
    row = (
        db.query(AiSetting)
        .filter(AiSetting.user_id == user.id)
        .first()
    )
    stored_key = None
    if row and row.encrypted_api_key:
        try:
            stored_key = decrypt_api_key(row.encrypted_api_key)
        except ValueError:
            stored_key = None

    api_key = payload.api_key or stored_key
    provider = payload.provider
    if provider == "qwen":
        base_url = payload.base_url or (row.base_url if row else None) or config.QWEN_BASE_URL
        model = payload.model or (row.model if row else None) or config.QWEN_MODEL
    else:
        base_url = payload.base_url or (row.base_url if row else None) or config.DEEPSEEK_BASE_URL
        model = payload.model or (row.model if row else None) or config.DEEPSEEK_MODEL

    if not api_key:
        return AiSettingsTestOut(ok=False, message="请先填写自己的 API Key")

    try:
        text = _call_llm(
            "你是一个连接测试助手。",
            "请只回复 OK",
            provider=provider,
            base_url=base_url,
            model=model,
            api_key=api_key,
        )
        return AiSettingsTestOut(ok=True, message=text.strip())
    except Exception as exc:
        return AiSettingsTestOut(ok=False, message=str(exc)[:300])
