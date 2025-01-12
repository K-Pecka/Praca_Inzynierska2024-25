from django.db import models

from django.utils.translation import gettext_lazy as _

from dicts.models import BaseModel
from users.models import UserProfile


class Trip(BaseModel):
    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='trips_as_creator',
        verbose_name=_('Właściciel'), help_text=_('Właściciel')),
    members = models.ManyToManyField(
        UserProfile,
        related_name='trips_as_member',
        verbose_name=_('Profil'), help_text=_('Profil'))
    budget = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        verbose_name=_("Budżet"), help_text=_("Budżet"))
    start_date = models.DateField(
        auto_now_add=True, # TODO: zmienić na czas lokalny a nie serwerowy
        verbose_name=_("Data rozpoczęcia"), help_text=_("Data rozpoczęcia"))
    end_date = models.DateField(
        auto_now=True, # TODO: zmienić na czas lokalny a nie serwerowy
        verbose_name=_("Data zakończenia"), help_text=_("Data zakończenia"))
    settings = models.JSONField(
        default=dict, # TODO: stworzyć defaultowe, customowe ustawienia
        verbose_name=_("Ustawienia"), help_text=_("Ustawienia"))

    @property
    def activities(self):
        return self.activities.all()

    class Meta:
        db_table = 'trips'
        verbose_name = 'Wycieczka'
        verbose_name_plural = 'Wycieczki'


class TripActivity(BaseModel):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Nazwa"), help_text=_("Nazwa"))
    budget = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        verbose_name=_("Budżet"), help_text=_("Budżet"))
    description = models.TextField(
        max_length=500,
        verbose_name=_("Opis"), help_text=_("Opis"))
    date = models.DateTimeField(
        auto_now_add=True, # TODO: zmienić na czas lokalny a nie serwerowy
        verbose_name=_("Data"), help_text=_("Data"))
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name=_('Wycieczka'), help_text=_('Wycieczka'))

    class Meta:
        db_table = 'trip_activities'
        verbose_name = 'Aktywność na wycieczce'
        verbose_name_plural = 'Aktywności na wycieczce'


class FYQ(BaseModel):
    class Meta:
        db_table = 'fyq'
        verbose_name = 'FYQ'
        verbose_name_plural = 'FYQ'
