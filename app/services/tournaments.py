from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from app.database.connection import get_connection
from app.config import BACKUP_PATH


def get_stats() -> Dict[str, Any]:
    conn = get_connection()
    try:
        return {
            "users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            "tournaments": conn.execute("SELECT COUNT(*) FROM tournaments").fetchone()[0],
            "registrations": conn.execute("SELECT COUNT(*) FROM registrations").fetchone()[0],
            "support_tickets": conn.execute("SELECT COUNT(*) FROM support_tickets").fetchone()[0],
        }
    finally:
        conn.close()


def make_backup() -> str:
    src = Path("data/modyx_gaming.db")
    if not src.exists():
        raise FileNotFoundError("قاعدة البيانات غير موجودة")
    backup_dir = Path(BACKUP_PATH)
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = backup_dir / f"modyx_backup_{timestamp}.db"
    out.write_bytes(src.read_bytes())
    return str(out)


def add_announcement(title: str, message: str, target_group_id: int = 0, created_by: int = 0) -> Dict[str, Any]:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO announcements (title, message, target_group_id, status, created_by) VALUES (?, ?, ?, 'scheduled', ?)",
            (title, message, target_group_id, created_by),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM announcements WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()
