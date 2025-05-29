import secrets
import pycountry
import requests
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from cloudinary_storage.storage import MediaCloudinaryStorage

from rest_framework.response import Response

from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dicts.models import BaseModel
from dicts.validators import validate_only_alphabetic
from trips.managers import TripManager, TicketManager, TripAccessTokenManager
from users.models import UserProfile


def validate_iso_currency(value):
    """Walidacja kodu waluty zgodnego z ISO 4217"""
    if not pycountry.currencies.get(alpha_3=value):
        available = [c.alpha_3 for c in pycountry.currencies]
        raise ValidationError(
            f"'{value}' nie jest prawidłowym kodem waluty. "
            f"Dostępne kody: {', '.join(available)}"
        )


class Trip(BaseModel):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )
    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="trips_as_creator",
        verbose_name=_("Właściciel"), help_text=_("Właściciel")
    )
    members = models.ManyToManyField(
        UserProfile,
        blank=True,
        related_name="trips_as_member",
        verbose_name=_("Profil"), help_text=_("Profil")
    )

    budget_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Budżet"), help_text=_("Budżet wycieczki")
    )

    start_date = models.DateField(
        verbose_name=_("Data rozpoczęcia"), help_text=_("Data rozpoczęcia")
    )
    end_date = models.DateField(
        verbose_name=_("Data zakończenia"), help_text=_("Data zakończenia")
    )
    settings = models.JSONField(
        default=dict,
        verbose_name=_("Ustawienia"), help_text=_("Ustawienia")
    )

    objects = TripManager()

    @property
    def activity_for_today(self):
        """Zwraca liczbę aktywności powiązanych z itineraries, które są aktywne dzisiaj"""
        today = timezone.now().date()
        count = 0
        for itinerary in self.itineraries.filter(start_date__lte=today, end_date__gte=today):
            count += itinerary.activities.count()
        return count

    @property
    def activity_for_week(self):
        """Zwraca liczbę aktywności powiązanych z itineraries kończących się w tym tygodniu"""
        today = timezone.now().date()
        days_until_sunday = 6 - today.weekday()
        end_of_sunday = today + timedelta(days=days_until_sunday)
        end_of_sunday = end_of_sunday if end_of_sunday <= today + timedelta(days=7) else today + timedelta(days=7)
        count = 0
        for itinerary in self.itineraries.filter(start_date__lte=today, end_date__range=(today, end_of_sunday)):
            count += itinerary.activities.count()
        return count

    @classmethod
    def add_member(cls, trip, user_profile):
        if trip.members.filter(id=user_profile.id).exists():
            return Response({"detail": "User is already a member of this trip."})
        trip.members.add(user_profile)
        return Response({"message": "User successfully added to the trip."})

    @classmethod
    def remove_member(cls, trip, user_profile):
        if not trip.members.filter(id=user_profile.id).exists():
            return Response({"detail": "User is not a member of this trip."}, status=400)
        trip.members.remove(user_profile)
        return Response({"message": "User successfully removed from the trip."})

    def check_if_is_member(self, profile):
        if self.members.filter(pk=profile.pk).exists():
            return True
        return False

    def check_if_is_pending(self, profile):
        if self.access_tokens.filter(trip=self, user_profile=profile, is_pending=True).exists():
            return True
        return False

    def get_itinerary_limit_for_user(self):
        """Zwraca maksymalną liczbę itineraries, które użytkownik może mieć"""
        if self.creator.type.code == "free":
            return 1
        elif self.creator.type.code == "tourist":
            return float('inf')
        elif self.creator.type.code == "guide":
            return float('inf')
        return 0

    def get_trip_limit_for_user(self):
        """Zwraca maksymalną liczbę wycieczek, które użytkownik może mieć"""
        if self.creator.type.code == "free":
            return 3
        elif self.creator.type.code == "tourist":
            return float('inf')
        elif self.creator.type.code == "guide":
            return float('inf')
        return 0

    def get_members_limit_for_user(self):
        """Zwraca maksymalną liczbę członków, których użytkownik może mieć w wycieczce"""
        if self.creator.type.code == "free":
            return 0
        elif self.creator.type.code == "tourist":
            return 5
        elif self.creator.type.code == "guide":
            return 30
        return 0

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia."))

        if self.pk and self.members.count() > self.get_trip_limit_for_user():
            raise ValidationError("Osiągnięto limit wycieczek dla tego użytkownika.")

        if not self.pk:
            if self.creator.trips_as_creator.count() >= self.get_trip_limit_for_user():
                raise ValidationError("Osiągnięto limit wycieczek dla tego użytkownika.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    objects = TripManager()

    class Meta:
        db_table = "trips"
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"


class TripAccessToken(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="access_tokens")
    token = models.CharField(max_length=24, verbose_name=_("Token"), help_text=_("Token"), unique=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="trip_access_tokens")
    is_pending = models.BooleanField(default=True, verbose_name=_("Czy oczekujący"), help_text=_("Czy oczekujący"))

    objects = TripAccessTokenManager()

    def generate_new_token(self):
        self.token = self.generate_token()
        self.save(update_fields=['token'])
        return self.token

    def change_status(self):
        self.is_pending = not self.is_pending
        self.save(update_fields=['is_pending'])
        return self.is_pending

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(18)[:24]

    @classmethod
    def get_token_by_profile(cls, profile):
        try:
            return cls.objects.get(user_profile=profile)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.trip} - {self.token}"

    class Meta:
        verbose_name = "Token dostępu do wycieczki"
        verbose_name_plural = "Tokeny dostępu do wycieczek"
        unique_together = ('trip', 'user_profile')


class TicketType(BaseModel):
    name = models.CharField(
        max_length=124,
        unique=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Typ biletu"
        verbose_name_plural = _("Typy biletów")


def get_default_ticket_type():
    return TicketType.objects.first()


class Ticket(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Nazwa"),
        help_text=_("Nazwa biletu"),
        null=True
    )
    file = models.FileField(
        storage=MediaCloudinaryStorage(),
        upload_to="tickets/",
        verbose_name=_("Bilet"),
        help_text=_("Bilet")
    )
    type = models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE,
        default=get_default_ticket_type,
        verbose_name=_("Typ"),
        help_text=_("Typ")
    )
    valid_from_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Ważny od daty"),
        help_text=_("Ważny od daty")
    )
    valid_from_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_("Ważny od godziny"),
        help_text=_("Ważny od godziny")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Wycieczka"),
        help_text=_("Wycieczka")
    )
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="owned_tickets",
        verbose_name=_("Właściciel"),
        help_text=_("Użytkownik, który dodał ten bilet")
    )
    profiles = models.ManyToManyField(
        UserProfile,
        related_name="shared_tickets",
        verbose_name=_("Udostępnione profile"),
        help_text=_("Profile, które mają dostęp do biletu"),
        blank=True,
        null=True
    )

    objects = TicketManager()

    class Meta:
        db_table = "tickets"
        verbose_name = "Bilet"
        verbose_name_plural = "Bilety"


class ExpenseType(BaseModel):
    name = models.CharField(
        max_length=124,
        unique=True,
        validators=[validate_only_alphabetic],
        verbose_name=_("Nazwa"),
        help_text=_("Nazwa")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Typ wydatku"
        verbose_name_plural = _("Typy wydatków")


def get_default_expense_type():
    return ExpenseType.objects.first()


class Expense(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name=_("Tytuł"),
        help_text=_("Tytuł wydatku")
    )
    amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Kwota wydatku"),
        help_text=_("Kwota wydatku")
    )
    currency = models.CharField(
        choices=[(c.alpha_3, c.name) for c in pycountry.currencies],
        max_length=3,
        default="PLN",
        verbose_name=_("Waluta"),
        help_text=_("Waluta wydatku")
    )
    date = models.DateField(
        verbose_name=_("Data"),
        help_text=_("Data wydatku"),
    )
    note = models.TextField(
        blank=True,
        verbose_name=_("Notatka"),
        help_text=_("Notatka dotycząca wydatku (opcjonalne)")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Podróż"),
        help_text=_("Powiązana podróż")
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Użytkownik"),
        help_text=_("Osoba, która poniosła wydatek"),
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        ExpenseType,
        on_delete=models.CASCADE,
        default=get_default_expense_type,
        verbose_name=_("Kategoria"),
        help_text=_("Kategoria wydatku")
    )

    @property
    def converted_amount(self):
        try:
            if self.currency == 'PLN':
                return round(self.amount, 2)

            response = requests.get(
                'https://api.frankfurter.app/latest',
                params={'from': self.currency, 'to': 'PLN'}
            )
            data = response.json()

            if 'rates' not in data:
                return round(self.amount, 2)

            rate = Decimal(list(data['rates'].values())[0])
            return round(self.amount * rate, 2)

        except Exception as e:
            print("Conversion error:", e)
            return None
    class Meta:
        db_table = "expenses"
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"


class DetailedExpense(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Nazwa wydatku"),
        help_text=_("NAME")
    )
    creator = models.ForeignKey(
        'users.UserProfile',
        on_delete=models.CASCADE,
        related_name='created_detailed_expenses',
        verbose_name=_("Twórca wydatku"),
        help_text=_("CREATOR")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Kwota"),
        help_text=_("AMOUNT")
    )
    currency = models.CharField(
        max_length=3,
        choices=[(c.alpha_3, c.name) for c in pycountry.currencies],
        default="PLN",
        verbose_name=_("Waluta"),
        help_text=_("CURRENCY")
    )
    amount_in_pln = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Kwota w PLN"),
        help_text=_("AMOUNT IN PLN")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="detailed_expenses",
        verbose_name=_("Wycieczka"), help_text=_("Wycieczka")
    )
    members = models.ManyToManyField(
        'users.UserProfile',
        related_name='detailed_expenses',
        verbose_name=_("Uczestnicy"),
        help_text=_("MEMBERS")
    )
    amount_per_member = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Kwota na osobę"),
        help_text=_("AMOUNT PER MEMBER")
    )
    amount_per_member_in_pln = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Kwota na osobę w PLN"),
        help_text=_("AMOUNT PER MEMBER IN PLN")
    )

    @property
    def convert_to_pln(self):
        try:
            response = requests.get(
                'https://api.frankfurter.app/latest',
                params={'from': self.currency, 'to': 'PLN'}
            )
            data = response.json()

            if 'rates' not in data:
                return round(self.amount, 2)

            rate = Decimal(list(data['rates'].values())[0])
            return round(self.amount * rate, 2)

        except Exception as e:
            print("Conversion error:", e)
            return None

    @classmethod
    def get_user_whole_debt(cls, user):
        """
        Zwraca całkowity dług użytkownika we wszystkich szczegółowych wydatkach.
        """
        total_debt = cls.objects.filter(members=user).aggregate(total=models.Sum('amount_per_member_in_pln'))['total']
        return total_debt if total_debt else Decimal('0.00')


    def calculate_shares(self):
        member_count = self.members.count()
        if member_count == 0:
            self.amount_per_member = Decimal('0')
            self.amount_per_member_in_pln = Decimal('0')
        else:
            self.amount_in_pln = self.convert_to_pln or Decimal('0')
            self.amount_per_member = self.amount / member_count
            self.amount_per_member_in_pln = self.amount_in_pln / member_count

    def clean(self):
        if self.pk:
            old = DetailedExpense.objects.get(pk=self.pk)
            if old.amount != self.amount:
                self.calculate_shares()

    def __str__(self):
        return f"{self.name} ({self.amount} {self.currency})"
