from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'name')
    empty_value_display = '-пусто-'
