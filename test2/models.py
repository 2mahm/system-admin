from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # Add new fields here
    birthdate = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)



    