#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_api.app import create_app
from flask_api.config.config_dev import Config

app = create_app(Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
