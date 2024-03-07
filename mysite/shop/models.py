from django.db import models
from .utilities import get_coordinates


class Shop(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=400)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="широта", editable=False)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="довгота", editable=False)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.latitude, self.longitude = get_coordinates(self.address)
        super().save(*args, **kwargs)


class CategoryProduct(models.Model):
    name = models.CharField(max_length=300)


class ProductShop(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=10)
    description = models.TextField()
    category = models.ForeignKey(CategoryProduct, on_delete=models.SET_NULL, null=True, blank=True)
