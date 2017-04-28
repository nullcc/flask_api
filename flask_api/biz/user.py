#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.security import check_password_hash
from ..database import db_session
from ..models.user import User


def get_user(username, password):
    session = db_session()
    user = session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
