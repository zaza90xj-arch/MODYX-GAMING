from __future__ import annotations

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.database.connection import initialize_database
from app.bot.main import router


async def create_dispatcher() -> Dispatcher:
    initialize_database()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    return dp


def run_bot() -> None:
    import asyncio

    if not BOT_TOKEN:
        print("BOT_TOKEN فارغ. أضف التوكن في app/config.py قبل التشغيل.")
        raise SystemExit(1)

    async def _main() -> None:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(_main())
