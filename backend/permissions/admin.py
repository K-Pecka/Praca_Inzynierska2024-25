from django.contrib import admin

from .models import CustomPermission


@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'can_view', 'can_edit', 'can_delete', 'is_active')

#test
