import unittest
from flask import Flask
from flask_testing import TestCase
import sys
sys.path.append('..')
from flask_api.app import create_app
from flask_api.config.config_dev import Config

Config.TESTING = True


class MyTest(TestCase):

    def create_app(self):
        app = create_app(Config)
        return app

    def test_posts(self):
        rv = self.client.get('/posts')
        print(rv.json)
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
