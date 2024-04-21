from django.contrib import admin
from .models import Shop, ProductShop
# Register your models here.

admin.site.register(ProductShop)
class ShopAdmin(admin.ModelAdmin):
    search_fields = ['address']

admin.site.register(Shop,ShopAdmin)
