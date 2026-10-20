from __future__ import annotations

from aiogram import Bot, Dispatcher
from app.bot.handlers import router as handlers_router
from app.config import BOT_TOKEN
from app.database.connection import initialize_database
from app.utils.logger import setup_logger
from app.utils.runtime_checks import validate_runtime_requirements

logger = setup_logger("modyx")


def run_bot() -> None:
    initialize_database()
    check = validate_runtime_requirements()
    if not check["ok"]:
        logger.warning("البوت متوقف: %s", "; ".join(check["issues"]))
        raise SystemExit(1)

    import asyncio

    async def _runner() -> None:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(handlers_router)
        await dp.start_polling(bot)

    asyncio.run(_runner())
