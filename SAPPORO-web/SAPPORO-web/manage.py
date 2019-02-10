#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        import django
        from django.core.management import execute_from_command_line
        from config.settings import DEVELOP, ALLOWED_HOSTS
        if DEVELOP:
            from django.core.management.commands.runserver import Command as runserver
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if DEVELOP:
        runserver.default_addr = ALLOWED_HOSTS[0]
    execute_from_command_line(sys.argv)
