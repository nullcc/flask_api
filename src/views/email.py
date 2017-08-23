#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ..utils.http import success
from src.tasks.email import send_welcome_email

bp = Blueprint('email', __name__)


@bp.route('/welcome', methods=['POST'])
def welcome():
    """
    演示使用celery异步任务队列发送邮件
    :return:
    """
    email = request.values.get("email")
    send_welcome_email.delay(email)
    return success()
