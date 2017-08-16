# -*- coding: utf-8 -*-

from functools import wraps


def after_action(after):
    """
    在函数运行后运行指定函数
    :param after:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            result = func(*args, **kwargs)
            after(result)
            return result
        return wrapped_function
    return decorator
