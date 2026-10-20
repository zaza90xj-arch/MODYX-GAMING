from __future__ import annotations

from app.database.connection import get_connection


def create_backup_record(file_name: str, status: str, message: str) -> dict:
    conn = get_connection()
    try:
        row = conn.execute(
            "INSERT INTO backup_logs (file_name, status, message) VALUES (?, ?, ?)",
            (file_name, status, message),
        )
        conn.commit()
        item = conn.execute("SELECT * FROM backup_logs WHERE id = ?", (row.lastrowid,)).fetchone()
        return dict(item)
    finally:
        conn.close()
