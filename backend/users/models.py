from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from permissions.models import CustomPermission
from .managers import CustomUserManager, CustomProfileManager
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


class UserProfile(BaseModel):
    class ProfileType(models.TextChoices):
        CLIENT = 'client', _("Client")
        GUIDE = 'guide', _("Guide")
        ADMIN = 'admin', _("Admin")
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="profile",
        verbose_name=_("Użytkownik"),
        help_text=_("Użytkownik")
    )
    type = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        choices=ProfileType.choices,
        default=ProfileType.CLIENT,
        verbose_name=_("Typ"),
        help_text=_("Typ profilu")
    )

    # objects = CustomProfileManager()

    def __str__(self):
        return f"{self.user}({str(self.type).upper()})"

    @property
    def created_trips(self):
        return self.trips_as_creator.all()

    @property
    def trips(self):
        return self.trips_as_member.all()

    def save(self, *args, **kwargs):
        if UserProfile.objects.filter(user=self.user, type=kwargs.get('type')).exists():
            raise ValidationError(_("Użytkownik może mieć tylko jeden profil (klient, przewodnik lub administrator)."))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Użytkownik")
        verbose_name_plural = _("Użytkownicy")
        db_table = "users"


class UserPermissions(BaseModel):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="profile_to_permission",
        verbose_name=_("Profil użytkownika"),
        help_text=_("Profil użytkownika")
    )
    permission = models.ForeignKey(
        CustomPermission,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Uprawnienia"),
        help_text=_("Uprawnienia"))

    def __str__(self):
        return f"UserProfilePermission: {self.profile} - {self.permission}"

    def __repr__(self):
        return f'<UserProfilePermission(id={self.id}, profile={self.profile}, permission={self.permission})>'

    class Meta:
        verbose_name = _("Uprawnienie użytkownika")
        verbose_name_plural = _("Uprawniania użytkowników")
        db_table = "profile_permissions"
        constraints = [
            UniqueConstraint(
                name="unique_user_permission",
                fields=["profile", "permission"],
            )
        ]
