from django.test import TestCase
from django.contrib.auth import get_user_model
User=get_user_model()
class UsersManagersTest(TestCase):
    def test_create_user(self):
        user=User.objects.create_user(email="user@mail.com", password="secret")
        self.assertEqual(user.email, "user@mail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)