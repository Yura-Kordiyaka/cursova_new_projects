from django.db import models
from user.models import User
from shop.models import ProductShop, Shop
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.geolocation import get_coordinates


class DefaultCategory(models.Model):
    name = models.CharField(max_length=200)
    date_add = models.DateTimeField(auto_now_add=True)


class UserCategory(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва категорії')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_default_categories(sender, instance, created, **kwargs):
        if created:
            default_categories = DefaultCategory.objects.all()
            for default_category in default_categories:
                UserCategory.objects.create(name=default_category.name, user=instance)


class UserShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=400)
    date_add = models.DateTimeField(auto_now_add=True ,null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="широта",editable=False)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="довгота",editable=False)

    def save(self, *args, **kwargs):
        self.latitude, self.longitude = get_coordinates(self.address)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserPurchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name_of_product = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва товару')
    description = models.TextField(blank=True, null=True)
    shop = models.ForeignKey(UserShop, on_delete=models.SET_NULL, blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_of_product


class DesiredPurchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_product = models.CharField(max_length=300, blank=True, null=True, verbose_name='назва товару')
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_of_product
