# -*- coding: utf-8 -*-

# 清除数据库数据

import sys
sys.path.append('.')
from flask_api.app import create_app
from flask_api.database import db_session
from flask_api.config.config_dev import DevConfig

app = create_app(DevConfig)
ctx = app.app_context()
ctx.push()

Post.query.delete()
User.query.delete()

db_session.commit()

print('数据清理完毕!')
