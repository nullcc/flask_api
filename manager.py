#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.app import create_app
from src.config.config_dev import DevConfig

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=DevConfig.PORT, debug=True)
