from __future__ import annotations

from app.config import AI_API_KEY, AI_MODEL


def ai_available() -> bool:
    return bool(AI_API_KEY and AI_MODEL)


def ai_status_message() -> str:
    if not ai_available():
        return "النظام الذكي غير مفعّل حاليًا. أضف AI_API_KEY وAI_MODEL في app/config.py."
    return f"المساعد الذكي جاهز: {AI_MODEL}"


def create_ai_reply(prompt: str) -> str:
    if not ai_available():
        return ai_status_message()
    return f"(محاكاة) تم استقبال طلب ذكي: {prompt[:150]}"
