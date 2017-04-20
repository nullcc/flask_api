# # -*- coding: utf-8 -*-
#
# import unittest
# from flask import Flask
# from flask_testing import TestCase
# import sys
# sys.path.append('..')
# from flask_api.app import create_app
# from flask_api.config.config_dev import Config
#
# Config.TESTING = True
#
#
# class PostTest(TestCase):
#
#     """
#     post接口测试
#     """
#
#     @staticmethod
#     def create_app():
#         app = create_app(Config)
#         return app
#
#     def test_posts(self):
#         rv = self.client.get('/posts')
#         assert rv.json['success']
#         assert rv.json['data'] is not None
#         assert rv.json['data'].get('posts') is not None
