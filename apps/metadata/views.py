from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .models import Metadata
from .serializers import MetadataSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "name"
    lookup_url_kwarg = "name"

    def get_queryset(self):
        # Only show metadata created by the current user
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Custom endpoint to search metadata by name or value
        """
        query = request.query_params.get("q", "")
        queryset = self.get_queryset().filter(
            Q(name__icontains=query) | Q(value__icontains=query)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
