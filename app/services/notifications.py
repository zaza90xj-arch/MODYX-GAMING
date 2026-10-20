from __future__ import annotations

from app.config import REGISTRATION_GROUP_ID


def send_registration_notice(request_no: str, tournament_name: str, status: str) -> dict:
    if not REGISTRATION_GROUP_ID:
        return {"ok": False, "message": "لم يتم ضبط معرف مجموعة التسجيلات. لا يمكن إرسال إشعار التسجيل."}
    return {
        "ok": True,
        "message": f"طلب جديد: {request_no} | البطولة: {tournament_name} | الحالة: {status}",
        "chat_id": REGISTRATION_GROUP_ID,
    }
