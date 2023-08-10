from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import UserProfile


def create_user(
        email='test@email.com', password='testpass123',
        first_name='first_test', last_name='last_test',
        username='test'):
    return get_user_model().objects.create_user(
        email=email, password=password, first_name=first_name,
        last_name=last_name, username=username)


class UsersManagersTests(TestCase):

    def test_create_user_and_userprofile(self):
        """Test creating a user and signal userprofile is successful."""
        user = create_user(email='normal@user.com')

        self.assertEqual(user.email, "normal@user.com")

        userprofile = UserProfile.objects.filter(user=user).exists()
        self.assertTrue(userprofile)

        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test create super user."""
        admin_user = get_user_model().objects.create_superuser(
            email="super@user.com", password="testpass123")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_delete_user_and_userprofile(self):
        """Test delete user and signal userprofile."""
        user = create_user()
        userprofile = UserProfile.objects.filter(user=user).exists()
        self.assertTrue(userprofile)

        user.delete()
        userprofile = UserProfile.objects.all().exists()
        self.assertFalse(userprofile)
