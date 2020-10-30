from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser, models.Model):
    code = models.CharField(max_length=20, unique=True)

class Model(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "owner")
	password = models.CharField(max_length = 200)
	name = models.CharField(max_length = 400)