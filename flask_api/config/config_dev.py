#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):

    # 调试模式
    DEBUG = True

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
    MAIL_DEFAULT_SENDER = ('Default Sender', 'zhangjinyi_ruby@163.com')
    ADMINS = ['89715089@qq.com', 'nullcc@gmail.com']

    # 错误日志发送配置
    SEND_LOGS = True
    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"

    # Redis
    # ------------------------------ #
    # If redis is enabled, it can be used for:
    #   - Sending non blocking emails via Celery (Task Queue)
    #   - Caching
    #   - Rate Limiting
    REDIS_ENABLED = False
    REDIS_URL = "redis://localhost:6379"  # or with a password: "redis://:password@localhost:6379"
    REDIS_DATABASE = 0

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    if not REDIS_ENABLED:
        CELERY_ALWAYS_EAGER = True

