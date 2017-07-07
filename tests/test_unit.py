# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append('.')
from flask_api.app import create_app
from flask_api.config.config_dev import DevConfig

app = create_app(DevConfig)
ctx = app.app_context()
ctx.push()

from unit import *

if __name__ == '__main__':
    unittest.main()
