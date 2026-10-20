from __future__ import annotations

import argparse
import asyncio

from app.config import BOT_TOKEN, WEB_HOST, WEB_PORT
from app.database.connection import initialize_database


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MODYX GAMING runner")
    parser.add_argument("--service", choices=["bot", "web", "both"], default="bot")
    return parser.parse_args()


async def start_bot() -> None:
    from app.bot.main import run_bot
    run_bot()


def start_web() -> None:
    import uvicorn
    uvicorn.run("app.web.routes.admin:app", host=WEB_HOST, port=WEB_PORT, reload=False)


def main() -> None:
    initialize_database()
    args = parse_args()

    if args.service == "bot":
        if not BOT_TOKEN:
            print("BOT_TOKEN فارغ. املأه في app/config.py قبل تشغيل البوت.")
            return
        start_bot()
    elif args.service == "web":
        start_web()
    else:
        if not BOT_TOKEN:
            print("BOT_TOKEN فارغ، سيتم تشغيل لوحة الويب فقط.")
        else:
            import threading
            thread = threading.Thread(target=start_bot, daemon=True)
            thread.start()
        start_web()


if __name__ == "__main__":
    main()
