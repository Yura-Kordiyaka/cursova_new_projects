from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('shop/product-search/<str:name_of_product>/', views.search_in_shop, name='search_in_shop')
]
