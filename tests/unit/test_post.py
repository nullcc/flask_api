# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from base_test import BaseTest
from flask_api.models.post import Post
from data.post import test_post1


class PostTest(BaseTest):

    @staticmethod
    def test_get_post():
        """
        查询post测试
        :return:
        """
        post = Post.get_post(test_post1.id)
        assert post is not None
        assert post.user_id == test_post1.id
        assert post.title == test_post1.title
        assert post.content == test_post1.content
