# coding: utf-8
import os
from distutils.util import strtobool
from pathlib import Path

from .local_settings import SECRET_KEY as LOCAL_SECRET_KEY


def str2bool(arg):
    if isinstance(arg, str):
        try:
            if strtobool(arg):
                return True
            else:
                return False
        except ValueError:
            raise Exception(
                "Please check your docker-compose.yml:environment, The bool value should be 'true value are y, yes, t, true, on and 1; false values are n, no, f, false, off and 0'")
    else:
        if arg:
            return True
        else:
            return False


BASE_DIR = Path(__file__).absolute().parent.parent
DEBUG = str2bool(os.environ.get("DEBUG", False))
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
ENABLE_USER_SIGNUP = str2bool(os.environ.get("ENABLE_USER_SIGNUP", True))

LOG_FILE_PATH = str(BASE_DIR.joinpath("../log/django.log").resolve())

if DEBUG:
    from .logging_config import local_info, local_debug
    if os.environ.get("LOG_LEVEL") == "DEBUG":
        LOGGING = local_debug
    else:
        LOGGING = local_info
else:
    from .logging_config import wsgi_info, wsgi_debug
    if os.environ.get("LOG_LEVEL") == "DEBUG":
        LOGGING = wsgi_debug
    else:
        LOGGING = wsgi_info

ALLOWED_HOSTS = ["*"]
SECRET_KEY = LOCAL_SECRET_KEY
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    str(BASE_DIR.joinpath("app/static")),
]

STATIC_ROOT = str(BASE_DIR.joinpath("static"))

LOGIN_URL = "/signin"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap4",
    "app",
]

BOOTSTRAP4 = {
    "include_jquery": True
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR.joinpath("templates")), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR.joinpath("db.sqlite3")),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": "database",
            "PORT": int(os.environ.get("POSTGRES_PORT")),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

if DEBUG:
    INTERNAL_IPS = ["172.21.0.1"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INSTALLED_APPS += [
        "debug_toolbar",
    ]
