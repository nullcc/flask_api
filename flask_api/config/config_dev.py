# -*- coding: utf-8 -*-


class DevConfig(object):

    # 调试模式
    DEBUG = True

    # secret key
    SECRET_KEY = 'secret key'

    # 运行端口号
    PORT = 5111

    # Mysql配置
    MYSQL_DATABASE_HOST = '127.0.0.1'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = '123456'
    MYSQL_DATABASE_DB = 'blog'
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
    MAIL_USERNAME = 'zhangjinyi_ruby@163.com'
    MAIL_PASSWORD = 'baicycle2017'
    MAIL_DEFAULT_SENDER = ('系统自动邮件', 'zhangjinyi_ruby@163.com')
    ADMINS = ['89715089@qq.com', 'nullcc@gmail.com']

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
    SQLALCHEMY_ECHO = True

    # 语言
    ACCEPT_LANGUAGES = {
        "en": "en_US",
        "zh-CN": "zh_Hans_CN",
        "ja": "ja_JP"
    }

    # 国际化本地语言
    BABEL_DEFAULT_LOCALE = 'en_US'  # en_US ja_JP zh_Hans_CN

    # 允许全局CORS
    ALLOW_GLOBAL_CORS = True

    # Flask-Session
    SESSION_TYPE = 'redis'

    # 时区
    TIME_ZONE = "Asia/Shanghai"

    def __init__(self):
        pass

    @classmethod
    def get_locale_by_accept_language(cls, accept_language):
        """
        通过请求头部的Accept-Language字段判断本地化语言，默认en_US
        :param accept_language:
        :return:
        """
        return cls.ACCEPT_LANGUAGES.get(accept_language, "en_US")
