from django.contrib import admin
from .models import Shop, ProductShop,CategoryProduct
# Register your models here.

admin.site.register(ProductShop)
admin.site.register(CategoryProduct)
class ShopAdmin(admin.ModelAdmin):
    search_fields = ['address']

admin.site.register(Shop,ShopAdmin)
