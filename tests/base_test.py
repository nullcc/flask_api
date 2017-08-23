# -*- coding: utf-8 -*-

import os
from flask_testing import TestCase
import sys
sys.path.append('.')
from src.app import create_app
from src.config.config_dev import DevConfig
from src.config.config_test import TestConfig
from src.config.config_production import ProductionConfig

if os.environ.get("debug_mode", None) == "True":
    config = TestConfig
elif os.environ.get("production_mode", None) == "True":
    config = ProductionConfig
else:
    config = DevConfig

config.TESTING = True


class BaseTest(TestCase):

    """
    测试基类
    """

    @staticmethod
    def create_app():
        app = create_app(config)
        return app
