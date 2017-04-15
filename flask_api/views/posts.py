#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, current_app as app
from mako.template import Template
from ..models.post import Post
from ..database import db_session
from ..utils.http import success, failed

bp = Blueprint('posts', __name__)


@bp.route('/new', methods=['GET'])
def new():
    return Template(filename='./flask_api/templates/post/new.html').render()


@bp.route('', methods=['GET'])
def index():
    session = db_session()
    posts = session.query(Post).all()
    posts = [post.to_dict() for post in posts]
    data = {'posts': posts}
    app.logger.info('hi')
    return success(data=data)


@bp.route('', methods=['POST'])
def create():
    title = request.values.get("title")
    content = request.values.get("content")
    session = db_session()
    new_post = Post(title=title, content=content)
    session.add(new_post)
    session.commit()
    session.close()
    return success()
