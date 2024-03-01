from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('authorization/', views.authorization_user, name='authorization')

]
