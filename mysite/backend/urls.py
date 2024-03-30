"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('all-category', views.all_category, name='all_category'),
    path('add-category', views.add_category, name='add_category'),
    path('category/<int:pk>/', views.get_product_by_category, name='get_product_by_category'),
    path('all_category/', views.all_category, name='all_category'),
    path('delete-purchase/<int:pk>/', views.delete_purchase, name='delete_purchase'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('add_purchase/', views.add_purchase, name='add_purchase'),
    path('purchase/<int:pk>/', views.specific_purchase, name='specific_purchase'),
    path('edit_purchase/<int:pk>/', views.edit_purchase, name='edit_purchase'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('costs/', views.user_costs, name='user_costs'),
    path('desired_purchase/', views.desired_purchase, name='desired_purchase'),
    path('add_user_shop/', views.add_user_shop, name='add_user_shop'),
    path('user_shop/', views.user_shops, name='users_shop'),
    path('shop/delete/<int:pk>/', views.delete_user_shop, name='delete_user_shop')
]
