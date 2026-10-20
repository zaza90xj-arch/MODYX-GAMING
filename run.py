from __future__ import annotations

import argparse
from pathlib import Path

from app.config import BOT_TOKEN, WEB_HOST, WEB_PORT
from app.database.connection import initialize_database


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MODYX GAMING launcher")
    parser.add_argument("service", choices=["bot", "web", "both"], nargs="?", default="bot")
    return parser.parse_args()


def main() -> None:
    initialize_database()
    args = parse_args()

    if not BOT_TOKEN and args.service in {"bot", "both"}:
        print("BOT_TOKEN فارغ. أضف التوكن داخل app/config.py قبل تشغيل البوت.")
        raise SystemExit(1)

    if args.service in {"bot", "both"}:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from app.bot.main import run_bot
        run_bot()

    if args.service in {"web", "both"}:
        import uvicorn
        uvicorn.run("app.web.routes.admin:app", host=WEB_HOST, port=WEB_PORT, reload=False)


if __name__ == "__main__":
    main()
