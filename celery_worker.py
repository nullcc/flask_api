#!/usr/bin/env python

"""
    运行celery，在根目录执行：
        celery -A celery_worker.celery --loglevel=info worker
"""

from src.config.config_dev import DevConfig
from src.app import create_app
from src.extensions import celery

app = create_app(DevConfig)
