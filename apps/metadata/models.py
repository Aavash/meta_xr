from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Metadata(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
