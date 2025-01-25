from django.db import models
from dicts.models import BaseModel
from trips.models import Trip


class Itinerary(BaseModel):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries')

    class Meta:
        db_table = "itineraries"
        verbose_name = "Wycieczka"
        verbose_name_plural = "Wycieczki"


class ItineraryActivity(BaseModel):

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField(max_length=5120)
    location = models.CharField(max_length=255)
    start_time = models.TimeField()
    duration = models.IntegerField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name="activities")

    class Meta:
        db_table = "itinerary_activities"
        verbose_name = "Aktywność"
        verbose_name_plural = "Aktywności"


