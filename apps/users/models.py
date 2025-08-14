# from django.db import models

# class User(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=50)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []