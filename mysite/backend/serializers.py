from .models import UserPurchases
from shop.models import Shop
from rest_framework import serializers


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class UserPurchaseSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = UserPurchases
        fields = ('id', 'price', 'name_of_product', 'shop', 'description','user','category')
