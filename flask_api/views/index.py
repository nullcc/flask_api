#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint, g, request, render_template, current_app as app
from ..utils.http import success, failed

bp = Blueprint('', __name__)
prefix = ''


@bp.route('/', methods=['GET'])
def index():
    return success()


@bp.route("/i18n", methods=['GET'])
def test():
    return render_template("i18n/i18n.html")
