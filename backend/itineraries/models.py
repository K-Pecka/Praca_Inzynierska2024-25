from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from dicts.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

from trips.models import Trip, Ticket
from itineraries.managers import ItineraryManager, ItineraryActivityManager


class Itinerary(BaseModel):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries', null=True, blank=True)

    objects = ItineraryManager()

    class Meta:
        db_table = "itineraries"
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"


class ItineraryActivityType(BaseModel):
    name = models.CharField(
        max_length=124,
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Typ aktywności planu"
        verbose_name_plural = _("Typy aktywności planu")

class ItineraryActivity(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    type = models.ForeignKey(
        ItineraryActivityType,
        on_delete=models.CASCADE,
        verbose_name=_("Typ"),
        help_text=_("Typ")
    )
    description = models.TextField(
        max_length=5120,
        verbose_name=_("Opis"),
        help_text=_("Opis"),
        null=True
    )
    location = models.CharField(
        max_length=255,
        verbose_name=_("Lokacja"),
        help_text=_("Lokacja"),
        null=True,
    )
    date = models.DateField(
        verbose_name=_("data"),
        help_text=_("data aktywności"),
    )
    start_time = models.TimeField(
        verbose_name=_("Czas zakończenia"),
        help_text=_("Czas rozpoczęcia"),
        null=True,
    )
    duration = models.IntegerField(
        verbose_name=_("Czas trwania"),
        help_text=_("Czas trawania"),
        null=True,
    )
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name=_("Plan"),
        help_text=_("Plan")
    )

    objects = ItineraryActivityManager()

    class Meta:
        db_table = "itinerary_activities"
        verbose_name = "Aktywność"
        verbose_name_plural = "Aktywności"

