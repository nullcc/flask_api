#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, render_template, current_app as app
from ..models.post import Post
from ..database import db_session
from ..utils.http import success, failed

bp = Blueprint('posts', __name__)


@bp.route('/new', methods=['GET'])
def new():
    return render_template('post/new.html')


@bp.route('', methods=['GET'])
def index():
    session = db_session()
    posts = session.query(Post).all()
    posts = [post.to_dict() for post in posts]
    data = {'posts': posts}
    return success(data=data)


@bp.route('', methods=['POST'])
def create():
    user_id = request.values.get("user_id")
    title = request.values.get("title")
    content = request.values.get("content")
    session = db_session()
    new_post = Post(user_id=user_id, title=title, content=content)
    session.add(new_post)
    session.commit()
    session.close()
    return success()
