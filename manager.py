#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_api.app import create_app
from flask_api.config.config_dev import DevConfig

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=DevConfig.PORT, debug=True)
