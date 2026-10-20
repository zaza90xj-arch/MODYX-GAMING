from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 بطولات", callback_data="tournaments")],
        [InlineKeyboardButton(text="📝 تسجيل", callback_data="register")],
        [InlineKeyboardButton(text="💬 الذكاء الاصطناعي", callback_data="ai")],
        [InlineKeyboardButton(text="⭐ النقاط", callback_data="points")],
    ])
