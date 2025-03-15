from django.core.validators import MinValueValidator
from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dicts.models import BaseModel
from trips.managers import TripManager, TicketManager
from users.models import UserProfile


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
    start_date = models.DateField(
        auto_now_add=True,  # TODO: zmienić na czas lokalny a nie serwerowy
        verbose_name=_("Data rozpoczęcia"), help_text=_("Data rozpoczęcia")
    )
    end_date = models.DateField(
        auto_now=True,  # TODO: zmienić na czas lokalny a nie serwerowy
        verbose_name=_("Data zakończenia"), help_text=_("Data zakończenia")
    )
    settings = models.JSONField(
        default=dict,  # TODO: stworzyć defaultowe, customowe ustawienia
        verbose_name=_("Ustawienia"), help_text=_("Ustawienia")
    )

    objects = TripManager()

    @property
    def budget(self):
        try:
            return Budget.objects.get(trip=self)
        except Budget.DoesNotExist:
            return Budget.objects.create(trip=self, currency='PLN')

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    objects = TripManager()

    class Meta:
        db_table = "trips"
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"


class TicketType(BaseModel):
    name = models.CharField(
        max_length=124,
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )

    def __str__(self):
        return self.name


def get_default_ticket_type():
    return TicketType.objects.first()


class Ticket(BaseModel):
    file = models.FileField(
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
    valid_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Ważny od"),
        help_text=_("Ważny od")
    )
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Profil"),
        help_text=_("Profil")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Wycieczka"),
        help_text=_("Wycieczka")
    )

    objects = TicketManager()

    class Meta:
        db_table = "tickets"
        verbose_name = "Bilet"
        verbose_name_plural = "Bilety"


class Budget(BaseModel):
    amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Kwota budżetu"),
        help_text=_("Kwota budżetu")
    )
    currency = models.CharField(
        max_length=10,
        verbose_name=_("Waluta"),
        help_text=_("Waluta (np. USD, PLN)")
    )
    trip = models.OneToOneField(
        Trip,
        on_delete=models.CASCADE,
        related_name="budżet",
        verbose_name=_("Wycieczka"),
        help_text=_("Powiązana wycieczka")
    )

    class Meta:
        db_table = "budgets"
        verbose_name = "Budżet"


class ExpenseType(BaseModel):
    name = models.CharField(
        max_length=124,
        verbose_name=_("Nazwa"),
        help_text=_("Nazwa")
    )

    def __str__(self):
        return self.name


def get_default_expense_type():
    return ExpenseType.objects.first()


class Currency(BaseModel):
    code = models.CharField(
        max_length=3,
        verbose_name=_("Kod waluty"),
        help_text=_("Kod waluty (np. PLN, EUR, USD)")
    )

    def __str__(self):
        return self.code

    class Meta:
        db_table = "currencies"
        verbose_name = "Waluta"
        verbose_name_plural = "Waluty"


def get_default_currency():
    currency = Currency.objects.first()
    if currency:
        return currency.id
    return None


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
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        default=get_default_currency,
        verbose_name=_("Waluta"),
        help_text=_("Waluta wydatku")
    )
    date = models.DateField(
        verbose_name=_("Data"),
        help_text=_("Data wydatku")
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

    class Meta:
        db_table = "expenses"
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"
