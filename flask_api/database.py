# -*- coding: utf-8 -*-

import os
import datetime
import functools
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_api.utils.utils import to_json_value
from flask_api.config.config_dev import DevConfig
from flask_api.config.config_test import TestConfig
from flask_api.config.config_production import ProductionConfig

if os.environ.get("debug_mode", None) == "True":
    config = TestConfig
elif os.environ.get("debug_mode", None) == "False":
    config = ProductionConfig
else:
    config = DevConfig

db_url = config.SQLALCHEMY_DATABASE_URI
engine = create_engine(db_url,
                       encoding="utf-8",
                       echo=False,
                       pool_size=5,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import flask_api.models
    Base.metadata.create_all(bind=engine)

