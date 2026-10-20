from __future__ import annotations

from aiogram import Bot, Dispatcher
from app.bot.handlers import router as handlers_router
from app.config import BOT_TOKEN
from app.utils.logger import setup_logger
from app.utils.runtime_checks import validate_runtime_requirements

logger = setup_logger("modyx.bot")


async def start_polling() -> None:
    requirements = validate_runtime_requirements()
    if not requirements["ok"]:
        logger.warning("تم إيقاف تشغيل البوت بسبب إعدادات غير مكتملة: %s", ", ".join(requirements["issues"]))
        raise SystemExit(1)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers_router)
    await dp.start_polling(bot)


def run_bot() -> None:
    import asyncio

    asyncio.run(start_polling())
