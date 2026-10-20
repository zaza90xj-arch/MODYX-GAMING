from __future__ import annotations

from app.database.connection import get_connection


def register_player(tournament_id: int, user_id: int, telegram_id: int, in_game_name: str, uid: str, participation_type: str = "solo", consent: int = 1) -> dict:
    conn = get_connection()
    try:
        exists = conn.execute(
            "SELECT 1 FROM registrations WHERE tournament_id = ? AND telegram_id = ? LIMIT 1",
            (tournament_id, telegram_id),
        ).fetchone()
        if exists:
            return {"ok": False, "message": "تم تسجيل اللاعب في هذه البطولة مسبقًا."}

        request_no = f"REQ-{telegram_id}-{tournament_id}"
        row = conn.execute(
            "INSERT INTO registrations (tournament_id, user_id, telegram_id, in_game_name, uid, participation_type, consent, status, request_no) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)",
            (tournament_id, user_id, telegram_id, in_game_name, uid, participation_type, consent, request_no),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM registrations WHERE id = ?", (row.lastrowid,)).fetchone()
        return {"ok": True, "registration": dict(item)}
    finally:
        conn.close()


def approve_registration(registration_id: int) -> dict:
    conn = get_connection()
    try:
        conn.execute("UPDATE registrations SET status = 'approved', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (registration_id,))
        conn.commit()
        return {"ok": True, "status": "approved"}
    finally:
        conn.close()


def reject_registration(registration_id: int) -> dict:
    conn = get_connection()
    try:
        conn.execute("UPDATE registrations SET status = 'rejected', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (registration_id,))
        conn.commit()
        return {"ok": True, "status": "rejected"}
    finally:
        conn.close()
