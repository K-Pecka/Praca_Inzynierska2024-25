from django.db import models

from django.utils.translation import gettext_lazy as _

from dicts.models import BaseModel
from permissions.managers import ActivePermissionsManager


class CustomPermission(BaseModel):
    code = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_("Kod uprawnienia"), help_text=_("Kod uprawnienia"))
    can_view = models.BooleanField(
        default=False,
        verbose_name=_("Czy ma dostęp do READ"), help_text=_("Czy ma dostęp do READ")
    )
    can_edit = models.BooleanField(
        default=False,
        verbose_name=_("Czy ma dostęp do WRITE"), help_text=_("Czy ma dostęp do WRITE")
    )
    can_delete = models.BooleanField(
        default=False,
        verbose_name=_("Czy ma dostęp do DELETE"), help_text=_("Czy ma dostęp do DELETE")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Czy aktywne"), help_text=_("Czy aktywne")
    )

    active_objects = ActivePermissionsManager()

    def perms_to_str(self):
        string = ""
        if self.can_view:
            string += "R"
        if self.can_edit:
            string += "W"
        if self.can_delete:
            string += "D"
        return string

    # @classmethod
    # def check_permission(cls, permission_code, action):
    #     return cls.active_objects.filter(code=permission_code, action=action).exists()

    @classmethod
    def get_active_item_by_name(cls, name):
        return cls.active_objects.filter(name=name)

    def __str__(self):
        return f"{self.code} / {self.perms_to_str()}"

    def __repr__(self):
        return f"<CustomPermission(pk={self.pk}, code={self.code})>"

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        verbose_name = "Uprawnienie"
        verbose_name_plural = "Uprawnienia"
        db_table = "permissions"
