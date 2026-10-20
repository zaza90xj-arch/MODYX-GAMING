from __future__ import annotations

from typing import Any, Dict

from app.database.connection import get_connection


def get_stats() -> Dict[str, Any]:
    conn = get_connection()
    try:
        stats = {
            "users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            "tournaments": conn.execute("SELECT COUNT(*) FROM tournaments").fetchone()[0],
            "registrations": conn.execute("SELECT COUNT(*) FROM registrations").fetchone()[0],
            "support_tickets": conn.execute("SELECT COUNT(*) FROM support_tickets").fetchone()[0],
        }
        return stats
    finally:
        conn.close()
