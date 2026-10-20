from __future__ import annotations

from app.database.connection import get_connection


def create_audit_entry(user_id: int, action: str, details: str, result: str) -> dict:
    conn = get_connection()
    try:
        row = conn.execute(
            "INSERT INTO audit_logs (user_id, action, details, result) VALUES (?, ?, ?, ?)",
            (user_id, action, details, result),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM audit_logs WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()
