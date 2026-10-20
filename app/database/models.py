from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional

from app.database.connection import get_connection


def ensure_user(telegram_id: int, first_name: str = "", last_name: str = "", username: str = "") -> Dict[str, Any]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)).fetchone()
        if row:
            return dict(row)
        cursor = conn.execute(
            "INSERT INTO users (telegram_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
            (telegram_id, first_name, last_name, username),
        )
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(user)
    finally:
        conn.close()


def get_user_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def create_tournament(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    try:
        row = conn.execute(
            """
            INSERT INTO tournaments (
                name, game_type, format_type, max_players, registration_open,
                status, start_time, end_time, description, rules,
                announcement_group_id, entry_requirements, creator_telegram_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("name"),
                data.get("game_type"),
                data.get("format_type"),
                int(data.get("max_players", 0)),
                int(data.get("registration_open", 1)),
                data.get("status", "upcoming"),
                data.get("start_time"),
                data.get("end_time"),
                data.get("description"),
                data.get("rules"),
                data.get("announcement_group_id"),
                data.get("entry_requirements"),
                data.get("creator_telegram_id"),
            ),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM tournaments WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()


def list_tournaments() -> list[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM tournaments ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_registration(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_connection()
    try:
        request_no = data.get("request_no") or f"REQ-{data['telegram_id']}-{data['tournament_id']}"
        row = conn.execute(
            """
            INSERT INTO registrations (
                tournament_id, user_id, telegram_id, in_game_name, uid,
                team_name, participation_type, contact_info, consent, status, request_no
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("tournament_id"),
                data.get("user_id"),
                data.get("telegram_id"),
                data.get("in_game_name"),
                data.get("uid"),
                data.get("team_name"),
                data.get("participation_type", "solo"),
                data.get("contact_info"),
                int(data.get("consent", 0)),
                data.get("status", "pending"),
                request_no,
            ),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM registrations WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()


def is_registration_duplicate(tournament_id: int, telegram_id: int) -> bool:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT 1 FROM registrations WHERE tournament_id = ? AND telegram_id = ? LIMIT 1",
            (tournament_id, telegram_id),
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def update_registration_status(registration_id: int, status: str) -> Dict[str, Any]:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE registrations SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, registration_id),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM registrations WHERE id = ?", (registration_id,)).fetchone()
        return dict(item)
    finally:
        conn.close()


def add_points(user_id: int, amount: int, reason: str, source: str = "manual", actor_id: int = 0, event_key: str = "") -> Dict[str, Any]:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO points_ledger (user_id, amount, reason, source, actor_id, event_key) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, amount, reason, source, actor_id, event_key),
        )
        conn.execute(
            "UPDATE users SET points = COALESCE(points, 0) + ?, level = MAX(1, CAST((COALESCE(points, 0) + ?) / 100 AS INTEGER) + 1), updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (amount, amount, user_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def create_support_ticket(user_id: int, subject: str, message: str) -> Dict[str, Any]:
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


def add_audit_log(user_id: int, action: str, details: str, result: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO audit_logs (user_id, action, details, result) VALUES (?, ?, ?, ?)",
            (user_id, action, details, result),
        )
        conn.commit()
    finally:
        conn.close()


def set_setting(key: str, value: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO app_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


def get_setting(key: str) -> Optional[str]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT value FROM app_settings WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
