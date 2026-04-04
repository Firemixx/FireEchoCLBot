import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


logs_path = Path(__file__).resolve().parents[1] / "Storage" / "logs.txt"

def config_log(level=logging.INFO):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    formatter = logging.Formatter(log_format)

    handler = RotatingFileHandler(
        logs_path,
        maxBytes=1_000_000,
        backupCount=0
    )

    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)

    logging.getLogger().addHandler(handler)