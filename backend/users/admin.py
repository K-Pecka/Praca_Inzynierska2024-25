from django.contrib import admin

from .models import AdminProfile, ClientProfile, GuideProfile, UserPermissions


@admin.register(AdminProfile)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("pk", "user")


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user")


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user")


@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "permission")

