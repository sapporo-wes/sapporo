#!/bin/bash
python3 /opt/NIG-web/NIG-web/manage.py makemigrations app
python3 /opt/NIG-web/NIG-web/manage.py migrate
