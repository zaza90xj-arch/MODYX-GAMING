from __future__ import annotations

from app.config import BOT_TOKEN, OWNER_TELEGRAM_ID
from app.utils.logger import setup_logger

LOGGER = setup_logger("modyx")


def validate_runtime_requirements() -> dict:
    issues = []
    if not BOT_TOKEN:
        issues.append("BOT_TOKEN فارغ. أضف توكن Telegram في app/config.py")
    if not OWNER_TELEGRAM_ID:
        issues.append("OWNER_TELEGRAM_ID فارغ. أضف معرف مالك المشروع")
    if issues:
        for msg in issues:
            LOGGER.warning(msg)
        return {"ok": False, "issues": issues}
    return {"ok": True, "issues": []}
