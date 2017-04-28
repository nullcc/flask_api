# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_api import app
from flask_api.utils.utils import to_dict

engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), encoding="utf-8", echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.to_dict = to_dict


def init_db():
    import flask_api.models
    Base.metadata.create_all(bind=engine)

