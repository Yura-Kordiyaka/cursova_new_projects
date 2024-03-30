from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('authorization/', views.authorization_user, name='authorization'),
    path('log_out/', views.log_out, name='log_out')

]
