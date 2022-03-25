from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    user_liked = models.IntegerField(verbose_name="liked",default=0)