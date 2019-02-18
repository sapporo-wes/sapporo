# coding: utf-8
import os
import random
import string
from distutils.util import strtobool
from .local_settings import SECRET_KEY as LOCAL_SECRET_KEY
from pathlib import Path


def str2bool(str):
    try:
        if strtobool(str):
            return True
        else:
            return False
    except ValueError:
        raise Exception(
            "Please check your docker-compose.yml:environment, The bool value should be 'true value are y, yes, t, true, on and 1; false values are n, no, f, false, off and 0'")


BASE_DIR = Path(__file__).absolute().parent.parent

ALLOWED_HOSTS = ["0.0.0.0"]
DEBUG = str2bool(os.environ.get("DEBUG"))
DEVELOP = str2bool(os.environ.get("DEVELOP"))
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE")
TIME_ZONE = os.environ.get("TIME_ZONE")
SECRET_KEY = LOCAL_SECRET_KEY
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
BASE_DIR.joinpath("static").mkdir(parents=True, exist_ok=True)
STATICFILES_DIRS = [
    str(BASE_DIR.joinpath("static")),
]

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

if DEVELOP:
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
    INTERNAL_IPS = ["172.24.0.1", "172.25.0.1"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INSTALLED_APPS += [
        "debug_toolbar",
    ]
