#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, current_app as app
from ..utils.http import success, failed

bp = Blueprint('', __name__)
prefix = ''


@bp.route('/', methods=['GET'])
def index():
    return success()

