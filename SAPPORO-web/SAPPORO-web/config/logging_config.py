# coding: utf-8
from .settings import LOG_FILE_PATH
from copy import deepcopy

TEMPLATE = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "default": {"format": "[%(asctime)s] %(levelname)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    },
        "long": {"format": "[%(asctime)s] %(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s",
                 "datefmt": "%Y-%m-%d %H:%M:%S",
                 },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# DUBUG is False --- console is filtered and django.server not work
wsgi_info = deepcopy(TEMPLATE)

wsgi_debug = deepcopy(TEMPLATE)
wsgi_debug["handlers"]["file"]["level"] = "DEBUG"
wsgi_debug["handlers"]["file"]["formatter"] = "long"
wsgi_debug["loggers"]["django"]["level"] = "DEBUG"

# DUBUG is True --- console is not filtered and django.server works
local_info = deepcopy(TEMPLATE)

local_debug = deepcopy(TEMPLATE)
local_debug["handlers"]["file"]["level"] = "DEBUG"
local_debug["handlers"]["file"]["formatter"] = "long"
local_debug["handlers"]["console"]["level"] = "DEBUG"
local_debug["handlers"]["console"]["formatter"] = "long"
local_debug["loggers"]["django"]["level"] = "DEBUG"
local_debug["loggers"]["django.server"]["level"] = "DEBUG"