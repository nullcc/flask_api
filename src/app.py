# -*- coding: utf-8 -*-

import os
import logging
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, g, render_template, request
from werkzeug.utils import find_modules, import_string
from flask_sqlalchemy import get_debug_queries
# 应用扩展
from src.extensions import (db, mail, redis_store, celery, cache, login_manager,
                                  limiter, cors, session, allows, api, toolbar, babel, gzip)

from flask import (template_rendered, request_started, request_finished,
                   got_request_exception, request_tearing_down)
from src.utils.signals import model_saved
from src.config import config as app_config

APP_NAME = 'src'
config = None


def create_app(conf=None):
    """
    创建flask app
    """
    global config
    app = Flask(APP_NAME, template_folder='src/templates')

    config = {}
    [config.__setitem__(k, getattr(conf, k)) for k in dir(conf) if not k.startswith('_')]

    configure_app(app, conf)
    register_blueprints('src.views', app)
    configure_celery_app(app, celery)
    configure_extensions(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_request_filter_handlers(app)
    configure_error_handlers(app)
    configure_logging(app)
    configure_db(app)

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
    def template_extras():
        """
        注入通用信息到模版
        :return:
        """
        # if g.user:
        #     return dict(current_user=g.user)
        return dict()


def configure_request_filter_handlers(app):
    """
    配置请求过滤器
    :param app:  app实例
    :return:
    """

    @app.before_request
    def before_request():
        print('before request handler')
        update_locale(app)
        login_manager.reload_user()
        # your before request code...

    @app.after_request
    def after_request(response):
        print('after request handler')
        # your after request code...
        # 记录请求中的慢查询
        for query in get_debug_queries():
            if query.duration > app.config['DATABASE_QUERY_TIMEOUT']:
                app.logger.warn(
                    ('Context: {}\nSLOW QUERY: {}\nParameters: {}\n'
                     'Duration: {}\n').format(query.context, query.statement, query.parameters, query.duration)
                )

        return response

    @app.teardown_request
    def teardown_request(response):
        db.session.close()  # 关闭db session
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
        from src.models.user import User
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

    # Flask-RESTful
    api.init_app(app)

    # Flask-Debugtoolbar
    # toolbar.init_app(app)

    # Flask-Babel
    babel.init_app(app)

    # Flask-Gzip
    gzip.init_app(app)


def configure_template_filters(app):
    """
    配置模版过滤器
    :param app:
    :return:
    """
    @app.template_filter('capitalize')
    def uppercase_filter(s):
        return s.capitalize()


def configure_db(app):
    """
    配置数据库
    :param app:
    :return:
    """
    from src.database import init_db, db_session
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

    logs_folder = os.path.join(app.root_path, os.pardir, "logs")
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

    # 慢查询日志
    slow_query_log = os.path.join(logs_folder, app.config['SLOW_QUERY_LOG'])
    slow_query_file_handler = logging.handlers.RotatingFileHandler(
        slow_query_log,
        maxBytes=100000,
        backupCount=10
    )
    slow_query_file_handler.setLevel(logging.WARN)
    slow_query_file_handler.setFormatter(formatter)
    app.logger.addHandler(slow_query_file_handler)

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


def update_locale(app):
    """
    更新当前请求locale
    :param app:  app实例
    :return:
    """
    language = request.accept_languages.best_match(app_config.ACCEPT_LANGUAGES)
    locale = app_config.get_locale_by_accept_language(language)
    app.config['BABEL_DEFAULT_LOCALE'] = locale
