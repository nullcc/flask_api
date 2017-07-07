# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from flask_api.models.user import User
from flask_api.app import create_app
from flask_api.config.config_dev import DevConfig
from flask.globals import _app_ctx_stack

test_user1 = User("nullcc", "123456", "nullcc@gmail.com", "1", id=1)

if not _app_ctx_stack.top:
    app = create_app(DevConfig)
    ctx = app.app_context()
    ctx.push()

    test_user1.save()

    _app_ctx_stack.pop()
