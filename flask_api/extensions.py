# -*- coding: utf-8 -*-

"""
    应用扩展
"""

from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_redis import FlaskRedis
from flask_cache import Cache
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
from flask_session import Session
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

# Login
login_manager = LoginManager()

# Rate Limiting
limiter = Limiter(auto_check=True, key_func=get_remote_address)

# CORS
cors = CORS()

# Session
session = Session()
