LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}][{asctime}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "file": {"class": "logging.FileHandler", "filename": "./logs/all.log", "formatter": "verbose"},
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
}
