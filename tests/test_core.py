from __future__ import annotations

import os


def sanitize_for_log(message: str) -> str:
    if not message:
        return ""
    # Remove obvious secrets in a straightforward way.
    for key in ("BOT_TOKEN", "AI_API_KEY", "WEB_ADMIN_PASSWORD"):
        value = os.environ.get(key)
        if value:
            message = message.replace(value, "[REDACTED]")
    return message


def test_database_initialization() -> None:
    from app.database.connection import initialize_database
    initialize_database()


def test_user_creation() -> None:
    from app.database.connection import get_connection
    conn = get_connection()
    try:
        conn.execute("DELETE FROM users WHERE telegram_id = 999999")
        conn.execute("INSERT INTO users (telegram_id, first_name, username) VALUES (?, ?, ?)", (999999, "Test", "demo"))
        conn.commit()
        row = conn.execute("SELECT telegram_id FROM users WHERE telegram_id = 999999").fetchone()
        assert row is not None
    finally:
        conn.close()


def test_duplicate_registration_prevention() -> None:
    from app.services.registrations import register_player
    result = register_player(1, 1001, 9001, "PlayerA", "UID-1", "solo", 1)
    assert result["ok"] is True
    result2 = register_player(1, 1002, 9001, "PlayerB", "UID-2", "solo", 1)
    assert result2["ok"] is False


def test_tournament_creation() -> None:
    from app.services.tournaments import create_turnament_record
    item = create_turnament_record("بطولة تجريبية", "solo", "1v1", 16, 1000)
    assert item["name"] == "بطولة تجريبية"


def test_ai_status_without_key() -> None:
    from app.services.ai_service import ai_status_message
    assert "غير مفعّل" in ai_status_message()


def test_security_redaction() -> None:
    from app.utils.security import sanitize_for_log
    assert "[REDACTED]" in sanitize_for_log("BOT_TOKEN=abc123")


def test_backup_log() -> None:
    from app.services.backups import create_backup_record
    record = create_backup_record("backup_test.db", "success", "ok")
    assert record["status"] == "success"
