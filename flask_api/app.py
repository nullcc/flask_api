# -*- coding: utf-8 -*-

import os
import logging
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, g, render_template
from werkzeug.utils import find_modules, import_string
from flask_babelplus import Babel
# 应用扩展
from flask_api.extensions import (db, mail, redis_store, celery, cache, login_manager,
                                  limiter, cors, session, scheduler, allows)

from flask import (template_rendered, request_started, request_finished,
                   got_request_exception, request_tearing_down)
from flask_api.utils.signals import model_saved

APP_NAME = 'FLASK_API'
config = None


def create_app(conf=None):
    """
    创建flask app
    """
    global config
    app = Flask(APP_NAME, template_folder='flask_api/templates')

    config = {}
    [config.__setitem__(k, getattr(conf, k)) for k in dir(conf) if not k.startswith('_')]

    configure_app(app, conf)
    register_blueprints('flask_api.views', app)
    configure_celery_app(app, celery)
    configure_extensions(app)
    # configure_template_filters(app)
    configure_context_processors(app)
    configure_request_filter_handlers(app)
    configure_error_handlers(app)
    configure_logging(app)
    configure_db(app)

    babel = Babel(app)

    configure_signals(app)

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


def configure_context_processors(app):
    """
    配置上下文处理器，返回的字典中的变量会被注入到模版中
    :param app:  app实例
    :return:
    """

    @app.context_processor
    def inject_user_info():
        """
        注入用户基本信息
        :return:
        """
        user = {'name': 'nullcc'}
        return dict(user=user)


def configure_request_filter_handlers(app):
    """
    配置请求过滤器
    :param app:  app实例
    :return:
    """

    @app.before_request
    def before_request():
        print('before request handler')
        login_manager.reload_user()
        # your before request code...

    @app.after_request
    def after_request(response):
        print('after request handler')
        # your after request code...
        return response

    @app.teardown_request
    def teardown_request(response):
        print('teardown request handler')
        # your teardown request code...
        return response


def configure_error_handlers(app):
    """
    错误处理
    :param app:  app实例
    :return:
    """
    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/forbidden_page.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/server_error.html'), 500


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

    # Flask-Cache
    cache.init_app(app)

    # Flask-Limiter
    limiter.init_app(app)

    # Flask-Cors
    if app.config.get('ALLOW_GLOBAL_CORS'):
        cors.init_app(app)

    # Flask-Session
    session.init_app(app)

    # Flask-APScheduler
    scheduler.init_app(app)
    scheduler.start()

    # # Flask-Login
    # login_manager.login_view = app.config["LOGIN_VIEW"]
    # login_manager.refresh_view = app.config["REAUTH_VIEW"]
    # login_manager.login_message_category = app.config["LOGIN_MESSAGE_CATEGORY"]
    # login_manager.needs_refresh_message_category = \
    #     app.config["REFRESH_MESSAGE_CATEGORY"]
    # login_manager.anonymous_user = Guest

    @login_manager.user_loader
    def load_user(user_id):
        """
        从数据库加载用户信息
        :param user_id:
        :return:
        """
        from flask_api.models.user import User
        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            g.user = user_instance
            return user_instance
        else:
            g.user = None
            return None

    login_manager.init_app(app)

    # Flask-Allows
    allows.init_app(app)


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
    if app.config.get('TESTING', None):  # 运行测试的时候不配置日志
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


def configure_signals(app):
    """
    配置信号
    :param app:
    :return:
    """
    # 模版渲染信号
    @template_rendered.connect_via(app)
    def log_template_renders(sender, template, context, **extra):
        sender.logger.debug('Rendering template "%s" with context %s',
                         template.name or 'string template',
                         context)

    # 请求开始信号
    @request_started.connect_via(app)
    def log_request(sender, **extra):
        sender.logger.debug('Request context is set up')

    # 请求结束信号
    @request_finished.connect_via(app)
    def log_response(sender, response, **extra):
        sender.logger.debug('Request context is about to close down.  '
                            'Response: %s', response)

    # 请求异常信号
    @got_request_exception.connect_via(app)
    def log_exception(sender, exception, **extra):
        sender.logger.debug('Got exception during processing: %s', exception)

    # 请求销毁信号
    @request_tearing_down.connect_via(app)
    def log_request_tearing_down(sender, **extra):
        sender.logger.debug('request tearing down')

    @model_saved.connect_via(app)
    def log_model_saved(sender, **extra):
        sender.logger.debug('model_saved!')
