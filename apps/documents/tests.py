from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Document

User = get_user_model()


class DocumentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="doc@example.com", password="docpass123", username="testdoc"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.test_file = SimpleUploadedFile("test_file.txt", b"Test file content")
        self.document = Document.objects.create(
            name="test_doc", file=self.test_file, uploaded_by=self.user
        )
        self.list_url = reverse("documents-list")
        self.detail_url = reverse(
            "documents-detail", kwargs={"name": self.document.name}
        )
        self.download_url = reverse(
            "documents-download", kwargs={"name": self.document.name}
        )

    def test_upload_document(self):
        new_file = SimpleUploadedFile("new_file.txt", b"New file content")
        data = {"name": "new_doc", "file": new_file}
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)

    def test_document_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_document_download(self):
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response["Content-Disposition"], 'attachment; filename="test_doc"'
        )

    def test_file_size_validation(self):
        large_file = SimpleUploadedFile(
            "large_file.txt",
            b"0" * (5 * 1024 * 1024 + 1),  # 5MB + 1 byte
        )
        data = {"name": "large_doc", "file": large_file}
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
