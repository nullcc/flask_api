# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from src.models.post import Post
from src.app import create_app
from src.config.config_dev import DevConfig
from flask.globals import _app_ctx_stack

test_post1 = Post(1, "测试标题1", "测试正文1", id=1)
test_post2 = Post(1, "测试标题2", "测试正文2", id=2)

if not _app_ctx_stack.top:
    app = create_app(DevConfig)
    ctx = app.app_context()
    ctx.push()

    test_post1.save()
    test_post2.save()

    _app_ctx_stack.pop()
