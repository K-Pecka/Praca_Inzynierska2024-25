from django.db import models
from dicts.models import BaseModel
from trips.models import Trip
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


class ItineraryActivity(BaseModel):
    CHOICES = [
        ("test1", "test1"),
        ("test2", "test2"),
        ("test3", "test3")
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=CHOICES)
    description = models.TextField(max_length=5120)
    location = models.CharField(max_length=255)
    start_time = models.TimeField()
    duration = models.IntegerField()
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name="activities")

    objects = ItineraryActivityManager()

    class Meta:
        db_table = "itinerary_activities"
        verbose_name = "Aktywność"
        verbose_name_plural = "Aktywności"
