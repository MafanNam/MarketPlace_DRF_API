from faker import Faker

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .test_setup import TestSetUp

from ..models import UserProfile

fake = Faker()

PROFILE_URL = reverse('accounts:profile')


def create_user(first_name='test_first', last_name='test_last',
                username='tests', email='test@gmail.com',
                password='testpass123', phone_number='+343 2424 5345',
                is_active=False, ):
    """Create and return a new user."""
    user = get_user_model().objects.create_user(
        first_name=first_name, last_name=last_name,
        username=username, email=email, password=password,
        phone_number=phone_number, is_active=is_active)
    user.save()
    return user


class TestAuthenticationViews(TestSetUp):

    def test_user_login_with_jwt_token(self):
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
        }
        user = create_user(**payload)
        user.is_active = True
        user.save()

        res = self.client.post(self.login_url, payload, format='json')
        token = res.data['access']

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in res.data)

        client = APIClient()
        # Bad credential
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        res = client.get(self.user_url, data={'format': 'json'})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # Good credentials
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = client.get(self.user_url, data={'format': 'json'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_registration_without_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_with_data(self):
        res = self.client.post(
            self.register_url, self.user_data, format='json')

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
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        email = response.data['email']
        user = get_user_model().objects.get(email=email)
        user.is_active = True
        user.save()
        res = self.client.post(
            self.login_url, self.user_data, format='json',
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PublicUserApiTests(TestSetUp):

    def test_user_profile_retrieve_unauthorized(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            first_name='test_first',
            last_name='test_last',
            username=fake.email().split('@')[0],
            email=fake.email(),
            password='testpass123',
            phone_number='+343 2424 5345',
            is_active=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_retrieve_success(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_user_profile_not_allowed(self):
        """Test POST is not allowed for the user profile endpoint"""
        res = self.client.post(PROFILE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_profile_particle_update(self):
        """Test POST is not allowed for the user profile endpoint"""
        payload = {'city': 'new_city'}
        res = self.client.patch(PROFILE_URL, payload, format='json')

        self.profile.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.city, payload['city'])
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(self.profile.oblast, profile.oblast)

    def test_user_profile_nested_particle_update(self):
        """Test POST is not allowed for the user profile endpoint"""
        payload = {'user': {'phone_number': '+543443'}}
        res = self.client.patch(PROFILE_URL, payload, format='json')

        self.profile.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.profile.user.phone_number, payload['user']['phone_number'])
        self.assertEqual(self.profile.user.phone_number,
                         self.user.phone_number)
