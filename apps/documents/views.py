from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from django.http import FileResponse
import os


class DocumentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "name"
    lookup_url_kwarg = "name"

    def get_queryset(self):
        # Only show documents uploaded by the current user
        return self.queryset.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=["get"])
    def download(self, request, name=None):
        document = self.get_object()
        file_path = document.file.path
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, "rb"), as_attachment=True, filename=document.name
            )
        return Response({"error": "File not found"}, status=404)
