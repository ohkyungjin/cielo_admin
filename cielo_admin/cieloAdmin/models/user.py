from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', '관리자'),
        ('staff', '직원'),
    ], default='staff')
