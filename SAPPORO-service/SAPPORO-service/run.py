#!/usr/local/bin/python3
# coding: utf-8
from app import create_app
from config import d_config, host, port

if __name__ == "__main__":
    app = create_app()
    app.config.from_mapping(d_config)
    app.run(host=host, port=port)
