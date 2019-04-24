#!/bin/bash
cd `dirname $0`
/bin/bash /opt/SAPPORO-web/wait-for database:5432
python3 /opt/SAPPORO-web/SAPPORO-web/config/generate_local_settings.py
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py makemigrations app
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py migrate
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py collectstatic --noinput
uwsgi /opt/SAPPORO-web/config/uwsgi.ini
