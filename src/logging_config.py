import logging.config
import os

LOG_DIR = "."
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[{asctime}] #{levelname:8} {filename}: {lineno} - {name} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname:8} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "mode": "a",
            "formatter": "detailed",
            "encoding": "utf-8",
            "level": "WARNING",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "sqlalchemy.engine": {  # Logger for SQLAlchemy engine
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
