from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self) -> None:
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:token_obtain_pair')
        self.user_url = reverse('accounts:user')

        self.user_data = {
            'first_name': 'test_first',
            'last_name': 'test_last',
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'phone_number': '456787',
            'is_active': True,
        }

        return super().setUp()
