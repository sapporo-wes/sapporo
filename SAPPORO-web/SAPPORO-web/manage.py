#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        import django
        from django.core.management.commands.runserver import Command as runserver
        from django.core.management import execute_from_command_line
        from config.env_loader import return_env_dict
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    env_dict = return_env_dict()
    django.setup()
    runserver.default_addr = env_dict["SAPPORO_web_HOST"]
    runserver.default_port = env_dict["SAPPORO_web_PORT"]

    execute_from_command_line(sys.argv)
