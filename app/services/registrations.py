from __future__ import annotations

from typing import Any, Dict, Optional

from app.database.connection import get_connection


def create_turnament_record(name: str, game_type: str, format_type: str, max_players: int, creator_telegram_id: int, description: str = "", rules: str = "") -> Dict[str, Any]:
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO tournaments (
                name, game_type, format_type, max_players, registration_open,
                status, description, rules, creator_telegram_id
            ) VALUES (?, ?, ?, ?, 1, 'upcoming', ?, ?, ?)
            """,
            (name, game_type, format_type, max_players, description, rules, creator_telegram_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM tournaments WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def open_registration(tournament_id: int) -> Dict[str, Any]:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE tournaments SET registration_open = 1, status = 'open', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (tournament_id,),
        )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()


def close_registration(tournament_id: int) -> Dict[str, Any]:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE tournaments SET registration_open = 0, status = 'closed', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (tournament_id,),
        )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()
