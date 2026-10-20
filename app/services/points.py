from __future__ import annotations

from app.database.connection import get_connection


def add_points(user_id: int, amount: int, reason: str, source: str = "manual", actor_id: int = 0, event_key: str = "") -> dict:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO points_ledger (user_id, amount, reason, source, actor_id, event_key) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, amount, reason, source, actor_id, event_key),
        )
        conn.execute(
            "UPDATE users SET points = COALESCE(points, 0) + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (amount, user_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return {"ok": True, "user": dict(row)}
    finally:
        conn.close()


def leaderboard(limit: int = 10) -> list:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT telegram_id, first_name, points FROM users ORDER BY points DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
