from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Metadata

User = get_user_model()


class MetadataTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="meta", email="meta@example.com", password="metapass123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.metadata = Metadata.objects.create(
            name="test_meta", value="test_value", created_by=self.user
        )
        self.list_url = reverse("metadata-list")
        self.detail_url = reverse(
            "metadata-detail", kwargs={"name": self.metadata.name}
        )

    def test_create_metadata(self):
        data = {"name": "new_meta", "value": "new_value"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Metadata.objects.count(), 2)

    def test_get_metadata_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_metadata(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_meta")

    def test_metadata_unique_name(self):
        data = {
            "name": "test_meta",  # Same name as existing
            "value": "duplicate",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
