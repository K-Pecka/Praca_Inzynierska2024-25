from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from permissions.models import CustomPermission
from .managers import CustomUserManager
from dicts.models import BaseModel
from dicts.validators import validate_only_alphabetic


class CustomUser(AbstractBaseUser, BaseModel):
    email = models.EmailField(
        unique=True,
        validators=[validate_email],
        verbose_name=_("Adres email"), help_text=_("Adres email użytkownika"))
    first_name = models.CharField(
        max_length=32,
        blank=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Imię"), help_text=_("Imię użytkownika"))
    last_name = models.CharField(
        max_length=32,
        blank=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Nazwisko"), help_text=_("Nazwisko użytkownika"))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Czy aktywny"), help_text=_("Czy użytkownik aktywny"))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Czy dostęp do admina"), help_text=_("Czy użytkownik ma dostęp do admina")
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_("Czy super użytkownik"), help_text=_("Czy super użytkownik")
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = []

    @property
    def is_admin(self):
        return hasattr(self, "adminprofile")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the app `app_label`.
        You can also override this method to apply custom logic.
        """
        return True


class BaseProfile(BaseModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="%(class)s",
        verbose_name=_("Użytkownik"),
        help_text=_("Użytkownik")
    )

    class Meta:
        abstract = True


class ClientProfile(BaseProfile):
    def __str__(self):
        return f"Client: {self.user}"

    def save(self, *args, **kwargs):
        if GuideProfile.objects.filter(user=self.user).exists() or AdminProfile.objects.filter(user=self.user).exists():
            raise ValidationError(_("Użytkownik może mieć tylko jeden profil (klient, menedżer lub administrator)."))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Klient")
        verbose_name_plural = _("Klienci")
        db_table = "clients"


class GuideProfile(BaseProfile):
    def __str__(self):
        return f"Przewodnik: {self.user}"

    def save(self, *args, **kwargs):
        if ClientProfile.objects.filter(user=self.user).exists() or AdminProfile.objects.filter(user=self.user).exists():
            raise ValidationError(_("Użytkownik może mieć tylko jeden profil (klient, menedżer lub administrator)."))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Menadżer")
        verbose_name_plural = _("Menadżerowie")
        db_table = "managers"


class AdminProfile(BaseProfile):
    def __str__(self):
        return f"Admin: {self.user}"

    def save(self, *args, **kwargs):
        if ClientProfile.objects.filter(user=self.user).exists() or GuideProfile.objects.filter(user=self.user).exists():
            raise ValidationError(_("Użytkownik może mieć tylko jeden profil (klient, menedżer lub administrator)."))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Administrator")
        verbose_name_plural = _("Administratorzy")
        db_table = "admins"


class UserPermissions(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="user_to_permissions",
        verbose_name=_("Użytkownik"), help_text=_("Użytkownik")
    )
    permission = models.ForeignKey(
        CustomPermission,
        on_delete=models.PROTECT,
        null=True,
        related_name="users",
        verbose_name=_("Uprawnienia"), help_text=_("Uprawnienia"))

    def __str__(self):
        return f"UserPermission: {self.user} - {self.permission}"

    def __repr__(self):
        return f'<UserPermission(id={self.id}, user={self.user}, permission={self.permission})>'

    class Meta:
        verbose_name = _("Uprawnienie użytkownika")
        verbose_name_plural = _("Uprawniania użytkowników")
        db_table = "user_permissions"
        constraints = [
            UniqueConstraint(
                name="unique_user_permission",
                fields=["user", "permission"],
            )
        ]
