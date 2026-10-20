from __future__ import annotations

from typing import Any, Dict, List

from app.database.connection import get_connection


def list_users() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def list_tournaments() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM tournaments ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def list_registrations() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM registrations ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_backup_log(file_name: str, status: str, message: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO backup_logs (file_name, status, message) VALUES (?, ?, ?)",
            (file_name, status, message),
        )
        conn.commit()
    finally:
        conn.close()
