#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from ..database import db_session


def transaction():
    def deco(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            session = db_session()
            session.begin(subtransactions=True)
            try:
                result = func(*args, **kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            return result
        return decorator
    return deco
