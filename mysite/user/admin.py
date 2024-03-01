from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'third_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def custom_username(self, obj):
        return obj.username

    custom_username.short_description = 'нік користувача'

    def custom_first_name(self, obj):
        return obj.first_name

    custom_first_name.short_description = "ім'я"

    def custom_last_name(self, obj):
        return obj.last_name

    custom_last_name.short_description = 'прізвище'


fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'third_name')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, CustomUserAdmin)