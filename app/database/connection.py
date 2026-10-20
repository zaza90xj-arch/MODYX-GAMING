from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH


def ensure_runtime_dirs() -> None:
    for path in [
        "data",
        "backups",
        "logs",
        "app/web/static",
        "app/web/templates",
        "app/bot/handlers",
        "app/bot/filters",
        "app/bot/middlewares",
        "app/bot/states",
        "app/security",
        "tests",
    ]:
        Path(path).mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_runtime_dirs()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                language TEXT DEFAULT 'ar',
                is_blocked INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_name TEXT NOT NULL,
                granted_by INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, role_name)
            );

            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                game_type TEXT NOT NULL,
                format_type TEXT NOT NULL,
                max_players INTEGER NOT NULL,
                registration_open INTEGER DEFAULT 1,
                status TEXT DEFAULT 'upcoming',
                start_time TEXT,
                end_time TEXT,
                description TEXT,
                rules TEXT,
                announcement_group_id INTEGER,
                entry_requirements TEXT,
                creator_telegram_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                telegram_id INTEGER NOT NULL,
                in_game_name TEXT,
                uid TEXT,
                team_name TEXT,
                participation_type TEXT,
                contact_info TEXT,
                consent INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                request_no TEXT UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS points_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                reason TEXT NOT NULL,
                source TEXT,
                actor_id INTEGER,
                event_key TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                message TEXT,
                target_group_id INTEGER,
                scheduled_for TEXT,
                status TEXT DEFAULT 'draft',
                created_by INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS support_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT,
                message TEXT,
                status TEXT DEFAULT 'open',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                result TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS backup_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                status TEXT,
                message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_group_id INTEGER UNIQUE,
                title TEXT,
                purpose TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS moderation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                moderator_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        default_roles = [
            ("Owner", "مالك المشروع"),
            ("Super Admin", "إدارة متقدمة"),
            ("Tournament Admin", "إدارة البطولات"),
            ("Moderator", "إدارة المجموعات"),
            ("Support", "الدعم"),
            ("Analyst", "الإحصاءات"),
        ]
        for role_name, description in default_roles:
            conn.execute(
                "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
                (role_name, description),
            )
        conn.commit()
    finally:
        conn.close()
