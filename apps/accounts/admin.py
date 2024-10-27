from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'created_at')
    readonly_fields = ('last_login', 'date_joined', 'profile_picture_preview')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': (
            'email', 'first_name', 'last_name', ('profile_picture', 'profile_picture_preview'),
            'birth_date'
        )}),
        ('Extra information', {'fields': ('password', 'last_login', 'date_joined', 'groups')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture', 'birth_date')
        }),
    )

    def profile_picture_preview(self, obj):
        return mark_safe(f'<img src="{obj.profile_picture.url}" width="75" height="75" />')

    profile_picture_preview.short_description = 'Preview'
