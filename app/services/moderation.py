from __future__ import annotations

from app.database.connection import get_connection


def add_group_record(telegram_group_id: int, title: str, purpose: str = "") -> dict:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO groups (telegram_group_id, title, purpose) VALUES (?, ?, ?) ON CONFLICT(telegram_group_id) DO UPDATE SET title = excluded.title, purpose = excluded.purpose",
            (telegram_group_id, title, purpose),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM groups WHERE telegram_group_id = ?", (telegram_group_id,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def add_moderation_log(group_id: int, action: str, details: str, moderator_id: int = 0) -> dict:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO moderation_logs (group_id, action, details, moderator_id) VALUES (?, ?, ?, ?)",
            (group_id, action, details, moderator_id),
        )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()
