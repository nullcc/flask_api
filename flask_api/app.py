# -*- coding: utf-8 -*-

from flask import Flask
from mako.template import Template
from werkzeug.utils import find_modules, import_string

# extensions
from flask_api.extensions import (db)

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
    # configure_celery_app(app, celery)
    configure_extensions(app)
    # configure_template_filters(app)
    # configure_context_processors(app)
    # configure_before_handlers(app)
    configure_errorhandlers(app)
    # configure_logging(app)

    return app


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


def configure_app(app, config):
    """
    配置app
    :param app:     app实例
    :param config:  配置对象
    :return:
    """
    app.config.from_object(config)


def configure_errorhandlers(app):
    """
    错误处理
    :param app:
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
    :param app:
    :return:
    """
    # Flask-SQLAlchemy
    db.init_app(app)
