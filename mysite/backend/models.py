from django.db import models
from user.models import User
from shop.models import ProductShop

class Category(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва категорії')

    def __str__(self):
        return self.name


class UserCategories(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва категорії')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class BudgetTracking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

