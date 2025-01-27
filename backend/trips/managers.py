from django.db import models
from django.db.models import Q

from rest_framework.exceptions import NotFound


class TripManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID")

    def by_user(self, profile):
        return self.filter(Q(creator=profile) | Q(members=profile)).distinct()


class TripActivityManager(models.Manager):
    def by_id_and_trip(self, pk, trip_pk):
        try:
            return self.get(pk=pk, trip=trip_pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono aktywności o podanym ID")

    def by_trip(self, trip_pk):
        return self.filter(trip=trip_pk).distinct()


class TicketManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono biletu o podanym ID")

    def by_user(self, profile):
        return self.filter(profile=profile).distinct()
