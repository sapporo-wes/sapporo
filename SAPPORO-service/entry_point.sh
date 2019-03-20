#!/bin/bash
python3 /opt/SAPPORO-service/SAPPORO-service/app/generate_local_config.py
uwsgi /opt/SAPPORO-service/config/uwsgi.ini
