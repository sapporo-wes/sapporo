#!/bin/sh
coverage run /opt/SAPPORO-web/SAPPORO-web/manage.py test app
coverage html
