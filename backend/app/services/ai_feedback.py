import json
import urllib.error
import urllib.request
from typing import Sequence

from .. import config
from ..ai_crypto import decrypt_api_key
from ..models import AiSetting, Feedback, Problem, Submission, User


def _local_feedback(
    submission: Submission,
    problem: Problem,
    result,
    missing_key: bool = False,
) -> Feedback:
    passed_count = sum(1 for item in result.results if item.passed)
    total_count = len(result.results)
    if result.status == "accepted":
        score = 95.0
        summary = "代码已通过全部测试用例，功能实现正确。"
    elif result.status == "wrong_answer":
        score = 68.0
        summary = "代码可以运行，但有测试用例没有通过，需要检查边界条件或输出格式。"
    else:
        score = 52.0
        summary = "代码运行出现错误，先检查语法、异常和输入处理。"

    lines = [
        "未配置自己的 API Key，当前使用本地规则反馈。" if missing_key else "",
        f"题目：{problem.title}",
        f"状态：{result.status}",
        f"测试通过：{passed_count}/{total_count}",
        summary,
        "",
        "改进建议：",
        "- 先阅读题目输入输出格式，逐行确认边界条件",
        "- 如果输出不一致，注意不要混入额外提示文本",
        "- 代码保持函数拆分清晰，变量命名有含义",
    ]
    if result.error_message:
        lines.extend(["", "错误信息：", result.error_message])
    return Feedback(
        submission_id=submission.id,
        feedback_text="\n".join(lines),
        score=score,
        provider="local",
    )


def _call_llm(
    system_prompt: str,
    user_prompt: str,
    provider: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> str:
    provider = provider or config.AI_PROVIDER
    if provider == "qwen":
        base_url = base_url or config.QWEN_BASE_URL
        model = model or config.QWEN_MODEL
        api_key = api_key or config.QWEN_API_KEY
    else:
        base_url = base_url or config.DEEPSEEK_BASE_URL
        model = model or config.DEEPSEEK_MODEL
        api_key = api_key or config.DEEPSEEK_API_KEY

    if not api_key:
        raise RuntimeError("AI API Key 未配置")

    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def resolve_user_ai_settings(db, user: User) -> dict | None:
    row = (
        db.query(AiSetting)
        .filter(AiSetting.user_id == user.id)
        .first()
    )
    if row and row.encrypted_api_key:
        try:
            api_key = decrypt_api_key(row.encrypted_api_key)
        except ValueError:
            api_key = None
        if api_key:
            if row.provider == "qwen":
                base_url = row.base_url or config.QWEN_BASE_URL
                model = row.model or config.QWEN_MODEL
            else:
                base_url = row.base_url or config.DEEPSEEK_BASE_URL
                model = row.model or config.DEEPSEEK_MODEL
            return {
                "provider": row.provider or "deepseek",
                "base_url": base_url,
                "model": model,
                "api_key": api_key,
            }

    if user.role == "teacher":
        if config.AI_PROVIDER == "qwen" and config.QWEN_API_KEY:
            return {
                "provider": "qwen",
                "base_url": config.QWEN_BASE_URL,
                "model": config.QWEN_MODEL,
                "api_key": config.QWEN_API_KEY,
            }
        if config.DEEPSEEK_API_KEY:
            return {
                "provider": "deepseek",
                "base_url": config.DEEPSEEK_BASE_URL,
                "model": config.DEEPSEEK_MODEL,
                "api_key": config.DEEPSEEK_API_KEY,
            }
    return None


def generate_feedback(
    db,
    submission: Submission,
    problem: Problem,
    result,
    user: User | None = None,
) -> Feedback:
    user_prompt = (
        "请以编程教学助手身份分析以下学生代码：\n\n"
        f"题目要求：\n{problem.description}\n\n"
        f"学生代码：\n{submission.code}\n\n"
        f"执行结果：\n{result.model_dump_json() if hasattr(result, 'model_dump_json') else str(result)}\n\n"
        "请从功能正确性、代码质量、性能优化和改进建议四个方面给出中文反馈，语气友好鼓励。"
    )
    settings = resolve_user_ai_settings(db, user) if user else None
    if settings:
        try:
            text = _call_llm(
                "你是一个严谨但友好的编程教学助手，请用简洁中文输出反馈。",
                user_prompt,
                **settings,
            )
            score = 95.0 if result.status == "accepted" else (68.0 if result.status == "wrong_answer" else 52.0)
            return Feedback(
                submission_id=submission.id,
                feedback_text=text.strip(),
                score=score,
                provider=settings["provider"],
            )
        except (urllib.error.URLError, KeyError, IndexError, RuntimeError, ValueError):
            return _local_feedback(submission, problem, result)
    return _local_feedback(submission, problem, result, missing_key=True)
