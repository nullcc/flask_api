# -*- coding: utf-8 -*-

# 清除数据库数据

import sys
sys.path.append('.')
from src.app import create_app
from src.database import db_session
from src.config.config_dev import DevConfig

from src.models.post import Post
from src.models.user import User

app = create_app(DevConfig)
ctx = app.app_context()
ctx.push()

Post.query.delete()
User.query.delete()

db_session.commit()

print('数据清理完毕!')
