from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
# Login ke liye ab username ki jagah email use hoga
    USERNAME_FIELD = 'email'
    # Superuser banate waqt username aur email dono mangega
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

