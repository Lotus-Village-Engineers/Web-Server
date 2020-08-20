from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, BusinessOwner, Customer


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = [
        'id',
        'email',
        'birthday',
        'phone_number',
        'date_joined',
        'is_active',
    ]
    # 어드민 페이지에서 유저모델 수정시 보여줄 필드를 지정한다.
    fieldsets = (
        # ('섹션명', '섹션에 포함될 필드')
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'birthday', 'phone_number', )}),
        ('Permissions', {'fields': ('is_admin', 'is_business_owner', )}),
        ('Important Dates', {'fields': ('last_login', )}),
    )
    # 어드민 페이지에서 신규 유저 생성시 보여줄 필드를 지정한다. (기본으로 username 사용하므로 수정 필요!)
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2')
        }),
        ('Personal Info', {'fields': ('name', 'birthday', 'phone_number', )}),
        ('Permissions', {'fields': ('is_business_owner', )}),
    )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(BusinessOwner)
admin.site.register(Customer)
