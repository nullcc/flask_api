#!/usr/bin/env python

"""
    运行celery，在根目录执行：
        celery -A celery_worker.celery --loglevel=info worker
"""

from flask_api.config.config_dev import Config
from flask_api.app import create_app
from flask_api.extensions import celery

app = create_app(Config)
