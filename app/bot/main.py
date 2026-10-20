from __future__ import annotations

from typing import Dict, Any

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.config import BOT_TOKEN, BOT_NAME
from app.database.connection import initialize_database, get_connection
from app.database.models import ensure_user
from app.services.ai_service import ai_status_message
from app.services.tournaments import create_turnament_record
from app.services.notifications import send_registration_notice

router = Router()


def main_menu_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 بطولات", callback_data="tournaments")],
        [InlineKeyboardButton(text="📝 تسجيل", callback_data="register")],
        [InlineKeyboardButton(text="💬 الذكاء الاصطناعي", callback_data="ai")],
        [InlineKeyboardButton(text="⭐ النقاط", callback_data="points")],
    ])
    return keyboard


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    ensure_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    await message.answer(
        f"مرحبًا بك في {BOT_NAME} 👋\n\nاختر الخدمة المطلوبة:",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == "tournaments")
async def tournaments_handler(callback: CallbackQuery) -> None:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT name, status FROM tournaments ORDER BY id DESC LIMIT 5").fetchall()
        if not rows:
            text = "لا توجد بطولات حالياً."
        else:
            text = "\n".join(f"• {r['name']} | {r['status']}" for r in rows)
    finally:
        conn.close()
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "ai")
async def ai_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(ai_status_message())
    await callback.answer()


@router.callback_query(F.data == "register")
async def register_handler(callback: CallbackQuery) -> None:
    await callback.message.answer("للتسجيل في بطولة، استخدم الأمر التالي في المستقبل: /register_tournament")
    await callback.answer()


@router.callback_query(F.data == "points")
async def points_handler(callback: CallbackQuery) -> None:
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    finally:
        conn.close()
    await callback.message.answer(f"عدد المستخدمين المسجلين: {row}")
    await callback.answer()


async def main() -> None:
    initialize_database()
    if not BOT_TOKEN:
        print("BOT_TOKEN فارغ. املأ قيمة BOT_TOKEN داخل app/config.py قبل التشغيل.")
        raise SystemExit(0)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
