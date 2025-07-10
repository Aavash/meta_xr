from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "username": "test",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")

    def test_user_registration(self):
        data = {
            "email": "testmeta@example.com",
            "username": "metatest",
            "password": "testpass123",
        }
        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("tokens" in response.data)

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_login_with_wrong_password(self):
        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "testpass",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_protected_endpoint_without_token(self):
        metadata_url = reverse("metadata-list")
        response = self.client.get(metadata_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
