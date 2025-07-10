from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Remove username field and use email as the username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Remove 'email' from REQUIRED_FIELDS

    def __str__(self):
        return self.email
