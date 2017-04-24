# -*- coding: utf-8 -*-

"""
    应用扩展
"""

from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_cache import Cache

from flask import current_app as app

# Database
db = SQLAlchemy()

# Mail
mail = Mail()

# Redis
redis_store = FlaskRedis()

# Celery
celery = Celery("tasks")

# Cache
cache = Cache()
