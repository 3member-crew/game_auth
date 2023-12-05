from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    score = models.IntegerField(default=0)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = [] 