from __future__ import annotations

from aiogram import Router
from aiogram.types import Message

from app.services.admin import list_support_tickets

router = Router()


@router.message(lambda message: message.text and message.text.startswith('/admin'))
async def admin_command(message: Message):
    tickets = list_support_tickets()
    if not tickets:
        await message.answer("لا توجد طلبات دعم حاليًا.")
        return
    lines = [f"#{t['id']} | {t['subject']} | {t['status']}" for t in tickets[:5]]
    await message.answer("طلبات الدعم:\n" + "\n".join(lines))
