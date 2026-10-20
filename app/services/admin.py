from __future__ import annotations

from typing import Any, Dict, List

from app.database.connection import get_connection


ROLE_PERMISSIONS = {
    "Owner": ["all"],
    "Super Admin": ["tournaments", "registrations", "results", "users", "points", "announcements", "settings"],
    "Tournament Admin": ["tournaments", "registrations", "results"],
    "Moderator": ["groups", "moderation", "support"],
    "Support": ["support"],
    "Analyst": ["stats", "reports"],
}


def grant_role(user_id: int, role_name: str, granted_by: int = 0) -> dict:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO user_roles (user_id, role_name, granted_by) VALUES (?, ?, ?)",
            (user_id, role_name, granted_by),
        )
        conn.commit()
        return {"ok": True, "role": role_name}
    finally:
        conn.close()


def has_permission(user_id: int, permission: str) -> bool:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT role_name FROM user_roles WHERE user_id = ?",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()
    roles = [r[0] for r in rows]
    for role in roles:
        perms = ROLE_PERMISSIONS.get(role, [])
        if "all" in perms or permission in perms:
            return True
    return False


def add_audit_log(user_id: int, action: str, details: str, result: str = "success") -> dict:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO audit_logs (user_id, action, details, result) VALUES (?, ?, ?, ?)",
            (user_id, action, details, result),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM audit_logs WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def list_audit_logs(limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
