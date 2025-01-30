from django.core.validators import MinValueValidator
from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dicts.models import BaseModel
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

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia."))

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "trips"
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"


class Ticket(BaseModel):
    ticket = models.FileField(
        upload_to="tickets/",
        verbose_name=_("Bilet"), help_text=_("Bilet")
    )
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Profil"), help_text=_("Profil")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Wycieczka"), help_text=_("Wycieczka")
    )

    class Meta:
        db_table = "tickets"
        verbose_name = "Bilet"
        verbose_name_plural = "Bilety"


class FYQ(BaseModel):
    class Meta:
        db_table = "fyq"
        verbose_name = "FYQ"
        verbose_name_plural = "FYQ"


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
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="budżet",
        verbose_name=_("Wycieczka"),
        help_text=_("Powiązana wycieczka")
    )

    class Meta:
        db_table = "budgets"
        verbose_name = "Budżet"


class Expense(BaseModel):
    EXPENSE_CHOICES = [
        ("test1", "test1"),
        ("test2", "test2"),
        ("test2", "test2"),
    ]

    amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Kwota wydatku"),
        help_text=_("Kwota wydatku")
    )
    date = models.DateField(
        verbose_name=_("Data"),
        help_text=_("Data wydatku")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Opis"),
        help_text=_("Opis wydatku (opcjonalne)")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Wycieczka"),
        help_text=_("Powiązana wycieczka")
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Użytkownik"),
        help_text=_("Osoba, która poniosła wydatek")
    )
    type = models.CharField(
        max_length=50,
        choices=EXPENSE_CHOICES,
        default="other",
        verbose_name=_("Rodzaj wydatku"),
        help_text=_("Rodzaj wydatku")
    )

    class Meta:
        db_table = "expenses"
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"
