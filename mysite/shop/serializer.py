from .models import ProductShop
from shop.models import Shop
from rest_framework import serializers


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class ProductShopSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = ProductShop
        fields = ('id', 'price', 'name', 'shop', 'description')
