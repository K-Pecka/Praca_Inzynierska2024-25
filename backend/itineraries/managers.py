from django.db.models import Q
from rest_framework.exceptions import NotFound

from django.db import models


class ItineraryManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono planu o podanym ID")

    def by_trip(self, trip_pk):
        return self.filter(trip=trip_pk).distinct()

    def by_trip_and_profile(self, trip_pk):
        return self.filter(
            Q(trip=trip_pk) | Q(profile=self.request.user.get_default_profile())
        ).distinct()


class ItineraryActivityManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono aktywności o podanym ID")

    def by_itinerary(self, itinerary_pk):
        return self.filter(itinerary=itinerary_pk).distinct()
