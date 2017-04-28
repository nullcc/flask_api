#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_api.app import create_app
from flask_api.config.config_test import TestConfig
from flask_api.config.config_production import ProductionConfig
import logging
import os

logger = logging.getLogger(__name__)

if os.environ.get("debug_mode", "False") == "True":
    logger.info("测试环境模式")
    config = TestConfig
else:
    config = ProductionConfig

application = create_app(config)

logger.info("started")
