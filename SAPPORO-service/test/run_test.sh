#!/bin/sh
coverage run -m unittest discover /opt/SAPPORO-service/SAPPORO-service
coverage report
coverage html
