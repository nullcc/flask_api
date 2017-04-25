# -*- coding: utf-8 -*-

"""
    异常类模块，定义常用异常信息
"""

from werkzeug.exceptions import HTTPException, Forbidden


class BaseError(HTTPException):
    """
    基础异常类
    """
    description = "An internal error has occured"


class AuthorizationRequired(BaseError, Forbidden):
    """
    需要访问权限
    """
    description = "Authorization is required to access this area."


class AuthenticationError(BaseError):
    """
    用户认证错误异常类
    """
    description = "Invalid username and password combination."

