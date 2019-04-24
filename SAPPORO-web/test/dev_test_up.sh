#!/bin/bash
rm -rf ../SAPPORO-web/db.sqlite3
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/migrate.sh
docker-compose -f docker-compose.dev.yml exec app python3 /opt/SAPPORO-web/SAPPORO-web/manage.py createsuperuser
docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/run_server.sh
