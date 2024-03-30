from django.db import models
from .geolocation import get_coordinates


class Shop(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=400)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="широта", editable=False)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="довгота", editable=False)

    def save(self, *args, **kwargs):
        self.latitude, self.longitude = get_coordinates(self.address)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CategoryProduct(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class ProductShop(models.Model):
    name = models.CharField(max_length=300)
    img = models.ImageField(upload_to="product_photo/%Y/%m/%d", verbose_name='головне фото',null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryProduct, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
