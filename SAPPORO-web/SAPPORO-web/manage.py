#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        import django
        from django.core.management.commands.runserver import Command as runserver
        from django.core.management import execute_from_command_line
        from config.env_loader import d_config
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    django.setup()
    runserver.default_addr = d_config["SAPPORO_web_HOST"]
    runserver.default_port = d_config["SAPPORO_web_PORT"]

    execute_from_command_line(sys.argv)
