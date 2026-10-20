from __future__ import annotations

from app.database.connection import get_connection


def list_support_tickets() -> list:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM support_tickets ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_ticket(user_id: int, subject: str, message: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO support_tickets (user_id, subject, message, status) VALUES (?, ?, ?, 'open')",
            (user_id, subject, message),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM support_tickets WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def update_ticket_status(ticket_id: int, status: str) -> dict:
    conn = get_connection()
    try:
        conn.execute("UPDATE support_tickets SET status = ? WHERE id = ?", (status, ticket_id))
        conn.commit()
        row = conn.execute("SELECT * FROM support_tickets WHERE id = ?", (ticket_id,)).fetchone()
        return dict(row)
    finally:
        conn.close()
