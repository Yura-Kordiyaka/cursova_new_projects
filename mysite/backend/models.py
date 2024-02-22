from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class User(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True,null=False, verbose_name='номер телефону')
    third_name = models.CharField(max_length=75, blank=True, null=True, verbose_name='по-батькові')

    def __str__(self):
        return self.username
