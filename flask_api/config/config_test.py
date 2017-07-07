#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TestConfig(object):

    # 调试模式
    DEBUG = False

    # secret key
    SECRET_KEY = 'secret key'

    # 运行端口号
    PORT = 5111

    # Mysql配置
    MYSQL_DATABASE_HOST = '127.0.0.1'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = '123456'
    MYSQL_DATABASE_DB = 'baicycle_police'
    MYSQL_DATABASE_CHARSET = 'utf8mb4'

    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(
        MYSQL_DATABASE_USER,
        MYSQL_DATABASE_PASSWORD,
        MYSQL_DATABASE_HOST,
        MYSQL_DATABASE_PORT,
        MYSQL_DATABASE_DB,
        MYSQL_DATABASE_CHARSET)

    # 数据库查询时间阈值
    DATABASE_QUERY_TIMEOUT = 0.5
    SQLALCHEMY_RECORD_QUERIES = True

    # flask_mail配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'YOUR EMAIL'
    MAIL_PASSWORD = 'YOUR EMAIL PASSWORD'
    MAIL_DEFAULT_SENDER = ('系统自动邮件', 'YOUR EMAIL')
    ADMINS = []

    # 错误日志发送配置
    SEND_LOGS = True
    DEBUG_LOG = "debug.log"
    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"
    SLOW_QUERY_LOG = "slow_query.log"

    # Redis
    REDIS_ENABLED = False
    REDIS_URL = "redis://localhost:6379"
    REDIS_DATABASE = 0

    # flask_cache配置
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 60

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    BROKER_URL = 'redis://localhost:6379/0'

    # 显示SQL执行情况
    SQLALCHEMY_ECHO = False

    # 国际化本地语言
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'  # en_US ja_JP

    # 允许全局CORS
    ALLOW_GLOBAL_CORS = True

    # Flask-Session
    SESSION_TYPE = 'redis'

    # Flask-APScheduler
    SCHEDULER_API_ENABLED = True

    # Flask-APScheduler Jobs
    # JOBS = [
    #     {
    #         'id': 'job1',
    #         'func': 'flask_api.tasks.job:job1',
    #         # 'args': (1, 2),
    #         'trigger': 'interval',
    #         'seconds': 5
    #     }
    # ]
