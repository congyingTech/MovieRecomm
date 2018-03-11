import unittest
from flask import current_app
from app import createApp, db


class BasicTestCase(unittest.TestCase):
    def setUp(self):#测试前运行
        self.app = createApp('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):#测试后运行
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):#测试执行——确保app存在
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):#测试执行——确保程序在测试配置中执行
        self.assertTrue(current_app.config['TESTING'])


