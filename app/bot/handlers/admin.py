from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.database.connection import get_connection
from app.services.tournaments import create_turnament_record

router = Router()


@router.callback_query(F.data == "tournaments")
async def tournaments_menu(callback: CallbackQuery):
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, name, status FROM tournaments ORDER BY id DESC LIMIT 10").fetchall()
    finally:
        conn.close()

    if not rows:
        text = "لا توجد بطولات مسجلة حاليًا."
    else:
        text = "\n".join(f"#{r['id']} | {r['name']} | {r['status']}" for r in rows)
    await callback.message.answer(text)
    await callback.answer()


@router.message(lambda message: message.text and "تجربة" in message.text)
async def demo_tournament(message: Message):
    created = create_turnament_record(
        name="بطولة تجريبية MODYX",
        game_type="solo",
        format_type="1v1",
        max_players=16,
        creator_telegram_id=message.from_user.id,
        description="بطولة تجريبية للشرح والتجربة فقط",
        rules="احترم القواعد وسيتم التحديث لاحقًا.",
    )
    await message.answer(f"تم إنشاء بطولة تجريبية بنجاح: #{created['id']} - {created['name']}")
