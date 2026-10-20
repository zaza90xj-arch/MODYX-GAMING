from __future__ import annotations

from app.config import BOT_TOKEN


def bot_config_valid() -> bool:
    return bool(BOT_TOKEN)
