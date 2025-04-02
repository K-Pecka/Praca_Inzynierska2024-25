from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import UserPermission, UserProfile, CustomUser

from dicts.helpers import get_admin_change_link


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'get_profile_link', 'is_active', 'is_guest', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_guest', 'is_staff', 'is_superuser'),
        }),
    )

    def get_profile_link(self, obj):
        if obj.get_default_profile() is not None:
            # Using reverse to generate the URL for the profile change page
            url = reverse('admin:users_userprofile_change', args=[obj.get_default_profile().pk])
            return mark_safe(f'<a href="{url}">{obj.get_default_profile()}</a>')  # Make it a hyperlink
        return "No profile"

    get_profile_link.short_description = 'Profile'

@admin.register(UserProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_select_related = ('user',)
    list_display = ("pk", "get_user_link")

    def get_user_link(self, obj):
        return get_admin_change_link(obj.user)

    get_user_link.short_description = 'User'



@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_select_related = ('profile', 'permission')
    list_display = ('pk', 'get_profile_link', 'get_permission_link')

    def get_profile_link(self, obj):
        return get_admin_change_link(obj.profile)

    get_profile_link.short_description = 'Profile'

    def get_permission_link(self, obj):
        return get_admin_change_link(obj.permission)

    get_permission_link.short_description = 'Permission'
    #a
