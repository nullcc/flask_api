#!/usr/bin/env python
# -*- coding: utf-8 -*-

from captcha.image import ImageCaptcha
from flask import Blueprint, Response
from ..utils.utils import gen_random_number_string

bp = Blueprint('captcha', __name__)


@bp.route('', methods=['GET'])
def get_captcha():
    """
    获取一个验证码
    :return:
    """
    image = ImageCaptcha()
    captcha = gen_random_number_string(4)
    # todo: cache the captcha
    data = image.generate(captcha)
    return Response(data, mimetype='image/jpeg')
