from .models import UserPurchases
from .models import UserShop
from shop.models import Shop
from rest_framework import serializers


class UserShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShop
        fields = "__all__"

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class UserPurchaseSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = UserPurchases
        fields = ('id', 'price', 'name_of_product', 'shop', 'description','user','category')
