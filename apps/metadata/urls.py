from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetadataViewSet

router = DefaultRouter()
router.register(r"", MetadataViewSet, basename="metadata")

urlpatterns = [
    path("", include(router.urls)),
]
