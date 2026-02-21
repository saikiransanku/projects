from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.FileField(upload_to='profile_images/', blank=True, null=True)
    address = models.TextField(blank=True, default='')
    land_survey_numbers = models.TextField(blank=True, default='')
    land_area_acres = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    soil_type = models.CharField(max_length=120, blank=True, default='')
    current_season = models.CharField(max_length=30, blank=True, default='')
    farmer_type = models.CharField(max_length=100, blank=True, default='')
    current_crop = models.CharField(max_length=120, blank=True, default='')
    plantation_date = models.DateField(blank=True, null=True)
    crop_end_time = models.TimeField(blank=True, null=True)
    passbook_image = models.FileField(upload_to='passbook_images/', blank=True, null=True)

    def __str__(self):
        return self.username


class UsageHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usage_entries')
    activity = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.activity}"
