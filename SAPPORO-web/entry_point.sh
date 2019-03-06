#!/bin/sh
curl -L https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /tmp/wait-for-it.sh
sh /tmp/wait-for-it.sh database:5432
python3 /opt/SAPPORO-web/SAPPORO-web/config/generate_local_settings.py
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py makemigrations app
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py migrate
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py collectstatic
uwsgi /opt/SAPPORO-web/config/uwsgi.ini
