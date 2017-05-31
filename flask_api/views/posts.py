#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, g, request, render_template, session as sess, current_app as app
from flask_cors import cross_origin
from ..models.post import Post
from ..database import db_session
from ..utils.http import success
from ..extensions import cache
from ..biz.post import do_something, insert_post
from ..utils.transaction import transaction

bp = Blueprint('posts', __name__)


@bp.route('/new', methods=['GET'])
def new():
    """
    创建新post页面
    :return:
    """
    return render_template('post/new.html')


@bp.route('', methods=['GET'])
# @cache.cached(timeout=60, key_prefix='posts')
def index():
    """
    演示cache
    :return:
    """
    session = db_session()
    posts = session.query(Post).all()
    posts = [post.to_dict() for post in posts]
    data = {'posts': posts}
    # print(sess.get('_session_id', 'not set'))
    # do_something()
    return success(data=data)


@bp.route('', methods=['POST'])
def create():
    """
    创建post
    :return:
    """
    user_id = request.values.get("user_id")
    title = request.values.get("title")
    content = request.values.get("content")
    new_post = Post(user_id=user_id, title=title, content=content)
    new_post.save()
    do_something()
    return success()


@bp.route('/sql', methods=['POST'])
@transaction()
def sql():
    """
    演示直接执行sql
    :return:
    """
    insert_post(1, 'title', 'content')
    return success()
