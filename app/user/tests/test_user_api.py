from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITests(TestCase):
    """Test users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@claiborne.com',
            'password': 'testpass',
            'name': 'Full Name'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Creating a user that already exists fails"""
        payload = {'email': 'test@claiborne.com', 'password': 'passtest'}
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must be more than 5 characters"""
        payload = {'email': 'test@claiborne.com', 'password': 'ppppp'}
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

        def test_create_token_for_user(self):
            """Test a token is created for user"""
            payload = {'email': 'test@claiborne.com', 'password': 'testpass'}
            create_user(**payload)
            response = self.client.post(TOKEN_URL, payload)

            self.assertIn('token', response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_create_token_with_invalid_credentials(self):
            """Test token is not created if invalid credentials given"""
            create_user(email='test@claiborne.com', password='testpass')
            payload = {'email': 'test@claiborne.com', 'password': 'wrong'}
            response = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', response.data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_with_no_user(self):
            """Test token is not created if no user is given"""
            payload = {'email': 'test@claiborne.com', 'password': 'testpass'}
            response = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', response.data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_with_no_fields(self):
            """Test email and password fields are required"""
            payload = {'email':'one', 'password': ''}
            response = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', response.data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
