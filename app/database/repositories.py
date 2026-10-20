import os
from datetime import datetime
from pathlib import Path

from app.config import BACKUP_PATH
from app.database.connection import get_connection


def make_backup() -> str:
    source = Path("data/modyx_gaming.db")
    if not source.exists():
        raise FileNotFoundError("قاعدة البيانات غير موجودة")
    backup_dir = Path(BACKUP_PATH)
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = backup_dir / f"modyx_backup_{timestamp}.db"
    with source.open("rb") as src, dest.open("wb") as dst:
        dst.write(src.read())
    return str(dest)


def backup_log(file_name: str, status: str, message: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO backup_logs (file_name, status, message) VALUES (?, ?, ?)",
            (file_name, status, message),
        )
        conn.commit()
    finally:
        conn.close()


def get_backup_logs() -> list:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM backup_logs ORDER BY id DESC LIMIT 20").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_announcement(title: str, message: str, target_group_id: int = 0, created_by: int = 0) -> dict:
    conn = get_connection()
    try:
        row = conn.execute(
            "INSERT INTO announcements (title, message, target_group_id, status, created_by) VALUES (?, ?, ?, 'scheduled', ?)",
            (title, message, target_group_id, created_by),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM announcements WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()


def list_announcements() -> list:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM announcements ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
