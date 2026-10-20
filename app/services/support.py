from __future__ import annotations

from app.database.connection import get_connection


def add_support_ticket(user_id: int, subject: str, message: str) -> dict:
    conn = get_connection()
    try:
        row = conn.execute(
            "INSERT INTO support_tickets (user_id, subject, message, status) VALUES (?, ?, ?, 'open')",
            (user_id, subject, message),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM support_tickets WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()
