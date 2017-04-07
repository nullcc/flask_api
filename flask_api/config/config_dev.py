#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = True
    PORT = 5000

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/blog'
