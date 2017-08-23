#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..models.post import Post
from ..database import db_session
from ..utils.transaction import transaction


def do_something():
    session = db_session()
    posts = session.query(Post).all()
    raise RuntimeError
    return True


@transaction()
def insert_post(user_id, title, content):
    lastrowid = db_session.execute("""
          insert into posts
            (user_id, title, content, views, status, created_time, updated_time)
          values
            (:user_id, :title, :content, 0, 1, now(), now())
        """, {"user_id": user_id, "title": title, "content": content}).lastrowid

    lastrowid = db_session.execute("""
          insert into posts
            (user_id, title, content, views, status, created_time, updated_time)
          values
            (:user_id, :title, :content, 0, 1, now(), now())
        """, {"user_id": user_id, "title": title, "content": content}).lastrowid
