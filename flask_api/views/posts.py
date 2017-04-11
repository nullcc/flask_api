#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, g, request, current_app as app
from mako.template import Template
import json
from ..models.post import Post, DBSession
from ..utils.http import success, failed
from flask_api.email import send_info

bp = Blueprint('posts', __name__)


@bp.route('/new', methods=['GET'])
def new():
    return Template(filename='./flask_api/templates/post/new.html').render()


@bp.route('', methods=['GET'])
def index():
    session = DBSession()
    posts = session.query(Post).all()
    posts = [post.to_dict() for post in posts]
    data = {'posts': posts}
    send_info.delay()
    # send_info()
    return success(data=data)


@bp.route('', methods=['POST'])
def create():
    title = request.values.get("title")
    content = request.values.get("content")
    session = DBSession()
    new_post = Post(title=title, content=content)
    session.add(new_post)
    session.commit()
    session.close()
    return success()
