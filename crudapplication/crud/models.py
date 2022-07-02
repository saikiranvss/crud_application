from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    address = models.CharField(max_length=255, null=True)
    device_type = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=32, null=True)
    country = models.CharField(max_length=32, null=True)
    zipcode = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)