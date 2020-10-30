from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser, models.Model):
    code = models.CharField(max_length=20, unique=True)