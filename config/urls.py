from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/metadata/", include("apps.metadata.urls")),
    path("api/documents/", include("apps.documents.urls")),
]
