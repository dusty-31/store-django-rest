from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTest(APITestCase):
    def register_user(self, username: str, password: str, role: str):
        url = reverse('register')
        data = {
            'username': username,
            'password': password,
            'role': role
        }
        return self.client.post(path=url, data=data, format='json')

    def test_user_registration(self):
        response = self.register_user(username='test_customer', password='12345', role='CUSTOMER')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_customer')
        self.assertEqual(User.objects.get().role, 'CUSTOMER')

    def test_register_username_exists(self):
        existing_user = self.register_user(username='test_customer', password='12345', role='CUSTOMER')
        new_user = self.register_user(username='test_customer', password='54321', role='CUSTOMER')
        self.assertEqual(existing_user.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_user.status_code, status.HTTP_400_BAD_REQUEST)
