# -*- coding: utf-8 -*-

from flask import url_for
from flask_api.extensions import db
from flask_api.utils.database import CRUDMixin
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .. import app

Base = declarative_base()


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict


class Post(Base, CRUDMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
DBSession = sessionmaker(bind=engine)
