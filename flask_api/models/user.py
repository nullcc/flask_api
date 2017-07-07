# -*- coding: utf-8 -*-

from datetime import datetime
from werkzeug.security import check_password_hash
from flask import url_for
from flask_api.extensions import db
from flask_api.utils.helpers import time_utcnow
from flask_api.utils.database import CRUDMixin, UTCDateTime
from flask_api.database import BaseModel
from sqlalchemy import Column, String
from ..database import Base, db_session
from .post import Post


class User(Base, BaseModel, CRUDMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    credit = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_time = db.Column(UTCDateTime(timezone=True), default=time_utcnow, nullable=False)
    updated_time = db.Column(UTCDateTime(timezone=True), default=time_utcnow, nullable=False)

    posts = db.relationship("Post", backref="user", lazy="dynamic")

    def __init__(self, username, password_hash, email, gender, *args, **kwargs):
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.gender = gender
        self.desc = ''
        self.credit = 0
        self.role = 'user'
        self.status = 1
        self.created_time = datetime.now()
        self.updated_time = datetime.now()
        if kwargs and kwargs['id']:
            self.id = kwargs['id']

    # Properties
    @property
    def is_active(self):
        """
        用户状态是否有效
        :return:
        """
        return self.status == 1

    @property
    def is_admin(self):
        """
        用户是否是管理员
        :return:
        """
        return self.role == 'admin'

    @classmethod
    def authenticate(cls, username, password):
        """
        用户认证
        :param username:
        :param password:
        :return:
        """
        session = db_session()
        user = session.query(User).filter_by(username=username).first()
        if user and user._verify_password(password):
            return user
        return None

    def all_posts(self):
        return Post.query.\
            filter(Post.user_id == self.id).\
            order_by(Post.id.desc()).all()

    def get_id(self):
        return self.id

    def _verify_password(self, password):
        """
        验证用户密码
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)
