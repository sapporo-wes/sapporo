#!/usr/local/bin/python3
# coding: utf-8
from app import create_app
from app.config import host, port

if __name__ == "__main__":
    app = create_app()
    app.run(host=host, port=port)
