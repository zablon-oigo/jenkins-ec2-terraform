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
        try:
            self.assertIsNone(user.username)
        
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="secret")

    def test_create_superuser(self):
        admin=User.objects.create_superuser(
            email="admin@mail.com",
            password="secret."
        )
        self.assertEqual(admin.email, "admin@mail.com")
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

        try:
            self.assertIsNone(admin.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@mail.com",
                password="secret.",
                is_superuser=False
            )
