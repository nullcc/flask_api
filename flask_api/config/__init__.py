# -*- coding: utf-8 -*-

import os
import pytz
from flask_api.config.config_dev import DevConfig
from flask_api.config.config_test import TestConfig
from flask_api.config.config_production import ProductionConfig

if os.environ.get("debug_mode", None) == "True":
    config = TestConfig
elif os.environ.get("production_mode", None) == "True":
    config = ProductionConfig
else:
    config = DevConfig

tz = pytz.timezone(config.TIME_ZONE)
