from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.config import BOT_NAME, BOT_TOKEN
from app.database.connection import get_connection
from app.services.ai_service import ai_status_message
from app.utils.logger import setup_logger

logger = setup_logger("modyx.bot")
router = Router()


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 بطولات Free Fire", callback_data="tournaments")],
        [InlineKeyboardButton(text="📝 تسجيل في بطولة", callback_data="register")],
        [InlineKeyboardButton(text="📊 بطولاتي", callback_data="my_tournaments")],
        [InlineKeyboardButton(text="⭐ النقاط والمستويات", callback_data="points")],
        [InlineKeyboardButton(text="💬 الذكاء الاصطناعي", callback_data="ai")],
        [InlineKeyboardButton(text="⚙️ الإعدادات", callback_data="settings")],
    ])


@router.message(CommandStart())
async def start_command(message: Message):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO users (telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
            (message.from_user.id, message.from_user.first_name or "", message.from_user.last_name or "", message.from_user.username or ""),
        )
        conn.commit()
    finally:
        conn.close()
    await message.answer(f"مرحبًا بك في {BOT_NAME} 👋\n\nاختر الخدمة المطلوبة:", reply_markup=main_menu_kb())


@router.message(Command("menu"))
async def menu_command(message: Message):
    await message.answer("القائمة الرئيسية:", reply_markup=main_menu_kb())


@router.message(Command("status"))
async def status_command(message: Message):
    conn = get_connection()
    try:
        users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        tournaments_count = conn.execute("SELECT COUNT(*) FROM tournaments").fetchone()[0]
    finally:
        conn.close()
    await message.answer(f"الحالة الحالية:\nالمستخدمون: {users_count}\nالبطولات: {tournaments_count}\nحالة البوت: {'مفعّل' if BOT_TOKEN else 'غير مفعّل'}")


@router.message(Command("register_tournament"))
async def register_tournament_command(message: Message):
    await message.answer("ميزة التسجيل في البطولات متاحة من لوحة الإدارة. يمكنك استخدام /menu للعودة للقائمة الرئيسية.")


@router.message(Command("ai_status"))
async def ai_status_command(message: Message):
    await message.answer(ai_status_message())


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("قائمة الأوامر:\n/start\n/menu\n/help\n/status\n/register_tournament\n/ai_status")
