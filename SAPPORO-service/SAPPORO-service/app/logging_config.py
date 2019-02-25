# coding: utf-8
from .config import LOG_FILE_PATH

wsgi_prod = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH
        },
        "wsgi": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["wsgi", "file"]
    },
}

wsgi_dev = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "long": {"format": "[%(asctime)s] %(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s",
                 "datefmt": "%Y-%m-%d %H:%M:%S",
                 },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "long",
            "filename": LOG_FILE_PATH
        },
        "wsgi": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "long",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["wsgi", "file"]
    },
}

local_prod = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "long": {"format": "[%(asctime)s] %(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s",
                 "datefmt": "%Y-%m-%d %H:%M:%S",
                 },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "long",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "long",
            "filename": LOG_FILE_PATH
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    },
}


local_dev = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "long": {"format": "[%(asctime)s] %(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s",
                 "datefmt": "%Y-%m-%d %H:%M:%S",
                 },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "long",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "long",
            "filename": LOG_FILE_PATH
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    },
}
