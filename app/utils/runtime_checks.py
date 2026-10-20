from __future__ import annotations

import os


def ensure_runtime_env() -> None:
    required = ["BOT_TOKEN", "OWNER_TELEGRAM_ID"]
    for name in required:
        if name == "BOT_TOKEN" and not os.environ.get(name):
            print("BOT_TOKEN فارغ. لا يمكن تشغيل البوت بدون توكن Telegram صالح.")
