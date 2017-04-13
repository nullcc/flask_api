#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, current_app as app
from ..utils.http import success, failed
from flask_api.tasks.email import send_welcome_email

bp = Blueprint('email', __name__)


@bp.route('', methods=['POST'])
def index():
    email = request.values.get("email")
    send_welcome_email.delay(email)
    return success()

