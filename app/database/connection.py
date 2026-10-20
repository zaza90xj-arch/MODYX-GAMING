import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH


def ensure_runtime_dirs() -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
    Path("backups").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    Path("app/web/static").mkdir(parents=True, exist_ok=True)
    Path("app/web/templates").mkdir(parents=True, exist_ok=True)
    Path("app/bot/handlers").mkdir(parents=True, exist_ok=True)
    Path("tests").mkdir(exist_ok=True)


SCHEMA = """
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

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_id INTEGER NOT NULL,
    name TEXT,
    score TEXT,
    result_text TEXT,
    winner TEXT,
    status TEXT DEFAULT 'pending',
    created_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    winner_team TEXT,
    score TEXT,
    notes TEXT,
    approved INTEGER DEFAULT 0,
    created_by INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS disputes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_id INTEGER,
    registration_id INTEGER,
    user_id INTEGER,
    title TEXT,
    message TEXT,
    status TEXT DEFAULT 'open',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
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

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_id INTEGER,
    name TEXT,
    captain_telegram_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    user_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    model TEXT,
    request_summary TEXT,
    status TEXT,
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

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    channel TEXT,
    sent INTEGER DEFAULT 0,
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

CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_tournaments_status ON tournaments(status);
CREATE INDEX IF NOT EXISTS idx_registrations_status ON registrations(status);
CREATE INDEX IF NOT EXISTS idx_points_user ON points_ledger(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
"""


def get_connection() -> sqlite3.Connection:
    ensure_runtime_dirs()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.execute(
            "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
            ("Owner", "مالك المشروع")
        )
        conn.execute(
            "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
            ("Super Admin", "إدارة متقدمة")
        )
        conn.execute(
            "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
            ("Tournament Admin", "إدارة البطولات")
        )
        conn.execute(
            "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
            ("Moderator", "إدارة المجموعات")
        )
        conn.execute(
            "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
            ("Support", "الدعم")
        )
        conn.execute(
            "INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)",
            ("Analyst", "الإحصاءات")
        )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized.")
