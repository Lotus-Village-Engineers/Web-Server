from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'birthday',
        'phone_number',
        'date_joined',
    )

admin.site.register(CustomUser, CustomUserAdmin)
