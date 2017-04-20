#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):

    # 调试模式
    DEBUG = True

    # secret key
    SECRET_KEY = 'secret key'

    # 运行端口号
    PORT = 5000

    # 数据库配置项
    DATABASE_HOST = '127.0.0.1'
    DATABASE_USERNAME = 'root'
    DATABASE_PASSWORD = '123456'
    DATABASE_PORT = '3306'
    DATABASE_NAME = 'blog'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DATABASE_USERNAME,
                                                                      DATABASE_PASSWORD,
                                                                      DATABASE_HOST,
                                                                      DATABASE_PORT,
                                                                      DATABASE_NAME)

    # flask_mail配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'zhangjinyi_ruby@163.com'
    MAIL_PASSWORD = 'baicycle2017'
    MAIL_DEFAULT_SENDER = ('系统自动邮件', 'zhangjinyi_ruby@163.com')
    ADMINS = ['89715089@qq.com', 'nullcc@gmail.com']

    # 错误日志发送配置
    SEND_LOGS = True
    DEBUG_LOG = "debug.log"
    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"

    # Redis
    REDIS_ENABLED = False
    REDIS_URL = "redis://localhost:6379"
    REDIS_DATABASE = 0

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_URL = 'redis://localhost:6379/0'

    # 显示SQL执行情况
    SQLALCHEMY_ECHO = True

    # 国际化本地语言
    BABEL_DEFAULT_LOCALE = 'en_US'  # en_US ja_JP zh_Hans_CN