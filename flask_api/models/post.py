# -*- coding: utf-8 -*-

from flask import url_for
from flask_api.extensions import db
from flask_api.utils.database import CRUDMixin
from sqlalchemy import Column, String
from ..database import Base


class Post(Base, CRUDMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

