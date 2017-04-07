#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Response, g
import json


# def error400(error_code, message, **kwargs):
#     return error_with_code(400, error_code, message, **kwargs)
#
#
# def error500(error_code, message, **kwargs):
#     return error_with_code(500, error_code, message, **kwargs)
#
#
# def error401(error_code, message, **kwargs):
#     return error_with_code(401, error_code, message, **kwargs)
#
#
# def error_with_code(status, code, message, **kwargs):
#     msg = dict(kwargs)
#     if not message:
#         message = error_codes.get_message_by_code(code)
#     if not code:
#         code = "inner_error"
#     msg["message"] = message
#     msg["code"] = code
#     return Response(response=json.dumps(msg), status=status, mimetype="application/json")


# def error(status, message, **kwargs):
#     """
#     返回错误提示(JSON格式):{"message":"错误信息"}
#     :param code:
#     :param message:
#     :return:
#     """
#     if 'code' not in kwargs:
#         return error_with_code(status=status, code='inner_error', message=message, **kwargs)
#
#     return error_with_code(status=status, message=message, **kwargs)


def success(**kwargs):
    """
    处理成功响应
    :param kwargs:
    :return:
    """
    result = dict(kwargs)
    result['success'] = True
    return Response(response=json.dumps(result), status=200, mimetype='application/json')


def failed(message, **kwargs):
    """
    处理失败响应
    :param message:
    :param kwargs:
    :return:
    """
    result = dict(kwargs)
    result['success'] = False
    result['message'] = str(message)
    return Response(response=json.dumps(result), status=200, mimetype='application/json')
