from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models, IntegrityError
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
        verbose_name=_("Adres email"),
        help_text=_("Adres email użytkownika")
    )
    first_name = models.CharField(
        max_length=32,
        blank=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Imię"),
        help_text=_("Imię użytkownika")
    )
    last_name = models.CharField(
        max_length=32,
        blank=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Nazwisko"),
        help_text=_("Nazwisko użytkownika")
    )
    date_of_birth = models.DateField(
        blank=True, null=True,
        verbose_name=_("Data urodzenia"),
        help_text=_("Data urodzenia")
    )
    is_guest = models.BooleanField(
        default=False,
        verbose_name=_("Czy gość"),
        help_text=_("Czy konto gościa")
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Czy aktywny"),
        help_text=_("Czy użytkownik aktywny")
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Czy dostęp do admina"),
        help_text=_("Czy użytkownik ma dostęp do admina")
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_("Czy super użytkownik"),
        help_text=_("Czy super użytkownik")
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = []

    @property
    def is_admin(self):
        return hasattr(self, "adminprofile")

    @property
    def is_guide(self):
        return self.get_default_profile().type == 'Przewodnik'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def create_guest_account(cls, name, email):
        try:
            user = cls.objects.create(
                email=email,
                first_name=f"{name}",
                last_name="",
                is_active=True,
                is_guest=True
            )
            return user
        except IntegrityError:
            raise ValueError("Użytkownik z tym adresem email już istnieje.")
        except ValidationError:
            raise ValueError("Niepoprawny adres email.")


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

    def get_default_profile(self):
        try:
            return UserProfile.objects.get(user=self, is_default=True)
        except UserProfile.DoesNotExist:
            raise ValueError("Nie znaleziono domyślnego profilu użytkownika.")

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = _("Użytkownicy")


class UserProfile(BaseModel):
    class ProfileType(models.TextChoices):
        CLIENT = 'client', _("Klient")
        GUIDE = 'guide', _("Przewodnik")
        ADMIN = 'admin', _("Administrator")
        GUEST = 'guest', _("Gość")

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profiles",
        verbose_name=_("Użytkownik"),
        help_text=_("Użytkownik")
    )
    type = models.CharField(
        max_length=32,
        blank=False,
        choices=ProfileType.choices,
        default=ProfileType.CLIENT,
        verbose_name=_("Typ"),
        help_text=_("Typ profilu")
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Czy jest podstawowym profilem"),
        help_text=_("Czy jest podstawowym profilem")
    )

    def __str__(self):
        return f"{self.user}({str(self.type).upper()})"

    @property
    def created_trips(self):
        return self.trips_as_creator.all()

    @property
    def trips(self):
        return self.trips_as_member.all()

    def save(self, *args, **kwargs):
        if self.pk:
            if self.is_default:
                UserProfile.objects.filter(user=self.user, is_default=True).update(is_default=False)
        else:
            if UserProfile.objects.filter(user=self.user, type=kwargs.get('type')).exists():
                raise ValidationError(_("Użytkownik może mieć tylko jeden profil (klient, przewodnik lub administrator)."))
            if not UserProfile.objects.filter(user=self.user, is_default=True):
                self.is_default = True

        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk:
            self.save()

        if self.user.is_guest:
            raise ValidationError(_("Nie można edytować profilu gościa."))


    class Meta:
        verbose_name = _("Profil")
        verbose_name_plural = _("Profile")
        db_table = "users"


class UserPermission(BaseModel):
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

    @classmethod
    def check_permission(cls, user_profile, perm_code, perm_action):
        """
        Check if the user has the given permission and action.
        This method can return a tuple of (is_allowed, message).
        """
        perm_to_user = cls.objects.filter(profile=user_profile, permission__code=perm_code).first()

        if not perm_to_user:
            return False, "Użytkownik nie posiada wymaganej zgody"

        if perm_action in perm_to_user.permission.actions():
            return True, "Dostęp do akcji został przyznany"

        return False, "Użytkownik nie ma uprawnień do wykonania tej akcji"

    def __str__(self):
        return f"UserProfilePermission: {self.profile} - {self.permission}"

    def __repr__(self):
        return f'<UserProfilePermission(pk={self.pk}, profile={self.profile}, permission={self.permission})>'

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
