from __future__ import annotations

import os


def sanitize_for_log(message: str) -> str:
    if not message:
        return ""
    for secret in ["BOT_TOKEN", "AI_API_KEY", "WEB_ADMIN_PASSWORD"]:
        value = os.environ.get(secret)
        if value:
            message = message.replace(value, "[REDACTED]")
    return message
