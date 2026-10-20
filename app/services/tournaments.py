from __future__ import annotations

from app.database.connection import get_connection


def create_turnament_record(name: str, game_type: str, format_type: str, max_players: int, creator_telegram_id: int) -> dict:
    conn = get_connection()
    try:
        row = conn.execute(
            "INSERT INTO tournaments (name, game_type, format_type, max_players, registration_open, status, creator_telegram_id) VALUES (?, ?, ?, ?, 1, 'upcoming', ?)",
            (name, game_type, format_type, max_players, creator_telegram_id),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM tournaments WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()


def open_registration(tournament_id: int) -> dict:
    conn = get_connection()
    try:
        conn.execute("UPDATE tournaments SET registration_open = 1, status = 'open' WHERE id = ?", (tournament_id,))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


def close_registration(tournament_id: int) -> dict:
    conn = get_connection()
    try:
        conn.execute("UPDATE tournaments SET registration_open = 0, status = 'closed' WHERE id = ?", (tournament_id,))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()
