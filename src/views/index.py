#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from ..utils.http import success

bp = Blueprint('', __name__)
prefix = ''


@bp.route('/', methods=['GET'])
def index():
    return success()


@bp.route("/i18n", methods=['GET'])
def i18n_test():
    """
    国际化测试
    :return:
    """
    return render_template("i18n/i18n.html")
