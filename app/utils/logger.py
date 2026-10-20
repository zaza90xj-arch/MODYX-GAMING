import logging
import re
from pathlib import Path


class SecretFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.patterns = [
            "BOT_TOKEN",
            "AI_API_KEY",
            "WEB_ADMIN_PASSWORD",
            "WEB_ADMIN_USERNAME",
        ]

    def filter(self, record):
        msg = str(record.getMessage())
        for key in self.patterns:
            msg = msg.replace(key, "[REDACTED]")
        record.msg = msg
        record.args = ()
        return True


def setup_logger(name: str = "modyx") -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(log_dir / "modyx.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.addFilter(SecretFilter())

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(SecretFilter())

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
