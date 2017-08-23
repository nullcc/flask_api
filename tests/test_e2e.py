# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append('.')
from src.app import create_app
from src.config.config_dev import DevConfig

app = create_app(DevConfig)
ctx = app.app_context()
ctx.push()

from e2e import *

if __name__ == '__main__':
    unittest.main()
