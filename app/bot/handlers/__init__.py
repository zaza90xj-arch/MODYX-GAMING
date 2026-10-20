from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.bot.keyboards.main import main_menu_kb
from app.config import BOT_NAME
from app.database.connection import get_connection
from app.database.models import ensure_user
from app.services.ai_service import ai_status_message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    ensure_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    await message.answer(
        f"مرحبًا بك في {BOT_NAME} 👋\nاختر الخدمة المطلوبة:",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(lambda c: c.data == "tournaments")
async def tournaments_handler(callback: CallbackQuery) -> None:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT name, status FROM tournaments ORDER BY id DESC LIMIT 5").fetchall()
        if rows:
            text = "\n".join(f"• {row['name']} | {row['status']}" for row in rows)
        else:
            text = "لا توجد بطولات حالياً."
    finally:
        conn.close()
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(lambda c: c.data == "register")
async def register_handler(callback: CallbackQuery) -> None:
    await callback.message.answer("ميزة التسجيل في البطولة متاحة من خلال القنوات الإدارية. ستتم إضافة واجهة تسجيل كاملة مستقبلاً.")
    await callback.answer()


@router.callback_query(lambda c: c.data == "ai")
async def ai_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(ai_status_message())
    await callback.answer()


@router.callback_query(lambda c: c.data == "points")
async def points_handler(callback: CallbackQuery) -> None:
    conn = get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    finally:
        conn.close()
    await callback.message.answer(f"عدد المستخدمين المسجلين: {total}")
    await callback.answer()
