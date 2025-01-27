from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'name')
    empty_value_display = '-пусто-'
