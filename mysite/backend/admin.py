from django.contrib import admin
from .models import DefaultCategory, UserCategory, UserPurchases, UserShop


# Register your models here.

@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(DefaultCategory)
class DefaultCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPurchases)
class UserPurchasesAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ['user','shop']


@admin.register(UserShop)
class ShopAdmin(admin.ModelAdmin):
    pass

