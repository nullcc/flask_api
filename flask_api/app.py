# -*- coding: utf-8 -*-

import os
import logging
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask
from mako.template import Template
from werkzeug.utils import find_modules, import_string
# 应用扩展
from flask_api.extensions import (db, mail, redis_store, celery)


APP_NAME = 'FLASK_API'
config = None


def create_app(conf=None):
    """
    创建flask app.
    :param conf: The configuration file or object.
                   The environment variable is weightet as the heaviest.
                   For example, if the config is specified via an file
                   and a ENVVAR, it will load the config via the file and
                   later overwrite it from the ENVVAR.
    """
    global config
    app = Flask(APP_NAME, template_folder='templates')
    config = {}
    [config.__setitem__(k, getattr(conf, k)) for k in dir(conf) if not k.startswith('_')]

    configure_app(app, conf)
    register_blueprints('flask_api.views', app)
    configure_celery_app(app, celery)
    configure_extensions(app)
    # configure_template_filters(app)
    # configure_context_processors(app)
    # configure_before_handlers(app)
    configure_error_handlers(app)
    configure_logging(app)
    configure_db(app)

    return app


def configure_app(app, conf):
    """
    配置app
    :param app:   app实例
    :param conf:  配置对象
    :return:
    """
    app.config.from_object(conf)


def register_blueprints(root, app):
    """
    注册蓝图
    :param root:  蓝图所在的目录名
    :param app:   app实例
    :return:
    """
    for name in find_modules(root, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            urls = name.split('.')
            # prefix = '/{}/{}'.format(urls[-2], urls[-1])
            if hasattr(mod, 'prefix'):
                prefix = mod.prefix
            else:
                prefix = '/{}'.format(urls[-1])
            app.register_blueprint(mod.bp, url_prefix=prefix)


def configure_celery_app(app, celery):
    """
    配置celery
    :param app:    app实例
    :param celery: celery实例
    :return:
    """
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


def configure_error_handlers(app):
    """
    错误处理
    :param app:  app实例
    :return:
    """
    @app.errorhandler(403)
    def forbidden_page(error):
        return Template(filename='./flask_api/templates/errors/forbidden_page.html').render(), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return Template(filename='./flask_api/templates/errors/page_not_found.html').render(), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return Template(filename='./flask_api/templates/errors/server_error.html').render(), 500


def configure_extensions(app):
    """
    配置扩展
    :param app:  app实例
    :return:
    """
    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Mail
    mail.init_app(app)

    # Flask-Redis
    redis_store.init_app(app)


def configure_db(app):
    from flask_api.database import init_db, db_session
    init_db()

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()


def configure_logging(app):
    """
    配置日志
    :param app:  app实例
    :return:
    """
    if app.config.get('TESTING', None):  # 跑测试的时候不配置日志
        return

    logs_folder = os.path.join(app.root_path, os.pardir, "flask_api/logs")
    from logging.handlers import SMTPHandler
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    # 普通信息日志
    info_log = os.path.join(logs_folder, app.config['INFO_LOG'])
    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    # 错误日志
    error_log = os.path.join(logs_folder, app.config['ERROR_LOG'])
    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log,
        maxBytes=100000,
        backupCount=10
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    # 调试日志
    if app.debug:
        debug_log = os.path.join(logs_folder, app.config['DEBUG_LOG'])
        debug_file_handler = logging.handlers.RotatingFileHandler(
            debug_log,
            maxBytes=100000,
            backupCount=10
        )
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(formatter)
        app.logger.addHandler(debug_file_handler)

    if app.config["SEND_LOGS"]:
        print('setup smtp server')
        mail_handler = \
            SMTPHandler(
                app.config['MAIL_SERVER'],
                app.config['MAIL_DEFAULT_SENDER'],
                app.config['ADMINS'],
                'application error, no admins specified',
                (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            )

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)

    if app.config["SQLALCHEMY_ECHO"]:
        # Ref: http://stackoverflow.com/a/8428546
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement,
                                  parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement,
                                 parameters, context, executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            app.logger.debug("Total Time: %f", total)
