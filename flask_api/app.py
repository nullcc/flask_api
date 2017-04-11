# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask
from mako.template import Template
from werkzeug.utils import find_modules, import_string

# 应用扩展
from flask_api.extensions import (db, mail, redis_store, celery)
from celery import Celery

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
            prefix = '/{}'.format(urls[-1])
            app.register_blueprint(mod.bp, url_prefix=prefix)


def configure_celery_app(app, celery):
    """
    配置celery
    :param app:    app实例
    :param celery: celery实例
    :return:
    """
    app.config.update({'BROKER_URL': app.config["CELERY_BROKER_URL"]})
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


def configure_logging(app):
    """
    配置日志
    :param app:  app实例
    :return:
    """
    logs_folder = os.path.join(app.root_path, os.pardir, "flask_api/flask_api/logs")
    from logging.handlers import SMTPHandler
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(logs_folder, app.config['INFO_LOG'])

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

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
