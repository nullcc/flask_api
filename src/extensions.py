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
from flask_allows import Allows
from flask_restful import Api
from flask_debugtoolbar import DebugToolbarExtension
from flask_babelplus import Babel
from .exts.flask_gzip import Gzip

from flask import g

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

# Flask-Allows
allows = Allows(identity_loader=lambda: g.user)

# Flask-RESTful
api = Api()

# Flask-Debugtoolbar
toolbar = DebugToolbarExtension()

# Flask-Babel
babel = Babel()

# Flask-Gzip
gzip = Gzip(compress_level=9)
