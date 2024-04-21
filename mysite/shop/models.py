from django.db import models
from .geolocation import get_coordinates


class Shop(models.Model):
    name = models.CharField(max_length=300,verbose_name="ім'я магазину")
    description = models.TextField(blank=True, null=True, verbose_name='опис магазину')
    address = models.CharField(max_length=400,verbose_name="Адреса")
    latitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="широта", editable=False)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="довгота", editable=False)

    def save(self, *args, **kwargs):
        self.latitude, self.longitude = get_coordinates(self.address)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Магазин"
        verbose_name_plural = "Магазини"






class ProductShop(models.Model):
    name = models.CharField(max_length=300, verbose_name="назва продукту")
    img = models.ImageField(upload_to="product_photo/%Y/%m/%d",null=True,blank=True, verbose_name="фото продукту")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ціна")
    description = models.TextField(verbose_name="опис продукту")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="назва магазину")

    def __str__(self):
        return f"продукт {self.name} магазину {self.shop.name}"

    class Meta:
        ordering = ("name",)
        verbose_name = "Продукт магазину"
        verbose_name_plural = "Продукти магазину"

