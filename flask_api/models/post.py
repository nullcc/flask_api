# -*- coding: utf-8 -*-

from datetime import datetime
from flask import url_for
from flask_api.extensions import db
from flask_api.utils.helpers import time_utcnow
from flask_api.utils.database import CRUDMixin, UTCDateTime
from sqlalchemy import Column, String
from ..database import Base


class Post(Base, CRUDMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_time = db.Column(UTCDateTime(timezone=True), default=time_utcnow, nullable=False)
    updated_time = db.Column(UTCDateTime(timezone=True), default=time_utcnow, nullable=False)

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.views = 0
        self.status = 1
        self.created_time = datetime.now()
        self.updated_time = datetime.now()
