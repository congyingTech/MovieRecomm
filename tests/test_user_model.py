import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    #测试password_setter把passwordset成功
    def test_password_setter(self):
        u = User(password='user')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='user')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='user')
        self.assertTrue(u.verify_password('user'))
        self.assertFalse(u.verify_password('user1'))

    def test_password_salts_are_random(self):
        u = User(password='user')
        u2 = User(password='user')
        self.assertTrue(u.password_hash != u2.password_hash)
