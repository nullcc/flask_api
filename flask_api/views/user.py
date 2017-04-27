#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, session as sess, current_app as app
from flask_cors import cross_origin
from flask_login import login_user, current_user
from ..models.user import User
from ..database import db_session
from ..utils.http import success, failed
from ..extensions import redis_store, limiter
from ..biz.user import get_user
from ..extensions import allows
from ..validators.permission import is_user, is_admin

bp = Blueprint('user', __name__)


@bp.route('/<int:user_id>', methods=['GET'])
@limiter.limit("5 per minute")
@cross_origin()
@allows.requires(is_user)
def show(user_id):
    """
    演示limiter,session,allows
    :param user_id:
    :return:
    """
    session = db_session()
    user = session.query(User).get(user_id)
    user_posts = user.all_posts()
    posts = [post.to_dict() for post in user_posts]
    user = user.to_dict()
    user['user_posts'] = posts
    # p = redis_store.pipeline()
    # p.set('user_' + str(user_id), 'abc')
    # p.execute()
    # p.get('user_2')
    # print(p.execute())
    sess['_session_id'] = 'flask_api_session_1'
    return success(user=user)


@bp.route('', methods=['POST'])
def create():
    """
    创建用户
    :return:
    """
    username = request.values.get("username")
    password = request.values.get("password")
    email = request.values.get("email")
    gender = int(request.values.get("gender"))
    desc = request.values.get("desc")
    session = db_session()
    user = User(username=username,
                password_hash=password,
                email=email,
                gender=gender,
                desc=desc)
    session.add(user)
    session.commit()
    session.close()
    return success()


@bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return:
    """
    username = request.values["username"]
    password = request.values["password"]
    user = get_user(username, password)
    if user:
        login_user(user)
        return success(data=user.to_dict())
    return failed(message='用户名或密码错误')
