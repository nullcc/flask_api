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
# class IndexTest(TestCase):
#
#     """
#     公共接口测试
#     """
#
#     @staticmethod
#     def create_app():
#         app = create_app(Config)
#         return app
#
#     def test_index(self):
#         rv = self.client.get('/')
#         assert rv.json['success']
