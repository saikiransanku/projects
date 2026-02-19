from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.FileField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username
