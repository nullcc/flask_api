#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, render_template, current_app as app
from ..models.user import User
from ..database import db_session
from ..utils.http import success, failed

bp = Blueprint('user', __name__)


@bp.route('/<int:user_id>', methods=['GET'])
def show(user_id):
    session = db_session()
    user = session.query(User).get(user_id)
    user_posts = user.all_posts()
    posts = [post.to_dict() for post in user_posts]
    user = user.to_dict()
    user['user_posts'] = posts
    return success(user=user)


@bp.route('', methods=['POST'])
def create():
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
