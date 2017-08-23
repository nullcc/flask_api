# -*- coding: utf-8 -*-

from datetime import datetime
from flask import url_for
from src.extensions import db
from src.utils.helpers import time_utcnow
from src.utils.database import UTCDateTime
from src.models.base import BaseModel
from sqlalchemy import Column, String
from ..database import Base


class Post(BaseModel):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_time = db.Column(UTCDateTime(timezone=True), default=time_utcnow, nullable=False)
    updated_time = db.Column(UTCDateTime(timezone=True), default=time_utcnow, nullable=False)

    def __init__(self, user_id, title, content, *args, **kwargs):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.views = 0
        self.status = 1
        self.created_time = datetime.now()
        self.updated_time = datetime.now()
        if kwargs and kwargs['id']:
            self.id = kwargs['id']

    @classmethod
    def get_post(cls, post_id):
        post = cls.query.get(post_id)
        return post
