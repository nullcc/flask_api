#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..database import db_session
from ..models.user import User


def get_user(username, password):
    session = db_session()
    user = session.query(User).filter_by(username=username,
                                         password_hash=password).first()
    return user
