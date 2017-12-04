from unittest import TestCase
from app.model import User, Role, Permission, AnonymousUser

class UserModelTest(TestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password is not None)

    def test_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.vertify('cat'))
        self.assertFalse(u.vertify('dog'))

    def test_password_random_salt(self):
        u1 = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertTrue(u1.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='123456@xxx.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARITICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))