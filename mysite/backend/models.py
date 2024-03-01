from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва категорії')

    def __str__(self):
        return self.name


class UserCategories(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва категорії')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LongitudeLatitude(models.Model):
    latitude = models.FloatField(verbose_name='довгота')
    longitude = models.FloatField(verbose_name='широта')


class BudgetTracking(models.Model):
    name = models.CharField(max_length=300, blank=True, null=False, verbose_name='керування фінансами')
    description = models.TextField(blank=True, null=True, verbose_name='опис витрачених грошей')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, blank=True, null=False, verbose_name='керування фінансами')
    longitude_Latitude = models.OneToOneField(LongitudeLatitude, on_delete=models.CASCADE,null=True,blank=True)
