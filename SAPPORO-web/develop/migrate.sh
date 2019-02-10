#!/bin/sh
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py makemigrations app
python3 /opt/SAPPORO-web/SAPPORO-web/manage.py migrate
