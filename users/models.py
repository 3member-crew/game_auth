from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        ordering = ['-score']   