from django.contrib.auth import get_user_model
from rest_framework import status

from .test_setup import TestSetUp


class TestAuthenticationViews(TestSetUp):

    def test_user_registration_without_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_with_data(self):
        res = self.client.post(self.register_url, self.user_data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        res = self.client.post(
            self.login_url, self.user_data, format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_verify_email(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        email = response.data['email']
        user = get_user_model().objects.get(email=email)
        user.is_active = True
        user.save()
        res = self.client.post(
            self.login_url, self.user_data, format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)