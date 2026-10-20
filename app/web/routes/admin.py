from __future__ import annotations

from app.database.connection import get_connection
from app.database.repositories import make_backup


def run_backup() -> dict:
    try:
        backup_path = make_backup()
        conn = get_connection()
        conn.execute(
            "INSERT INTO backup_logs (file_name, status, message) VALUES (?, 'success', 'Backup completed successfully')",
            (backup_path,),
        )
        conn.commit()
        conn.close()
        return {"ok": True, "path": backup_path}
    except Exception as exc:
        conn = get_connection()
        conn.execute(
            "INSERT INTO backup_logs (file_name, status, message) VALUES (?, 'error', ?)",
            ("unknown", str(exc)),
        )
        conn.commit()
        conn.close()
        return {"ok": False, "message": str(exc)}
