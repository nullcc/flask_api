#!/usr/bin/env python
# -*- coding: utf-8 -*-


def is_user(user, request):
    """
    判断角色是否是user
    :param user:
    :param request:
    :return:
    """
    return user.role == 'user'


def is_admin(user, request):
    """
    判断角色是否是admin
    :param user:
    :param request:
    :return:
    """
    return user.role == 'admin'
