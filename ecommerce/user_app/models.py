from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type = models.CharField(max_length=30, choices=(("customer", "customer"), ("admin", "admin"),), default = "customer")
