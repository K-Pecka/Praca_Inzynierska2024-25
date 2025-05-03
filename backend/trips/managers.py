from django.db import models
from django.db.models import Q

from rest_framework.exceptions import NotFound


class TripManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wycieczki o podanym ID")

    def by_user_profile(self, profile):
        return self.filter(Q(creator=profile) | Q(members=profile)).distinct()

    def by_user_and_trip(self, profile):
        return self.by_user_profile(profile)


class TicketManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono biletu o podanym ID")

    def by_user(self, profile):
        return self.filter(
            models.Q(owner=profile) | models.Q(profiles=profile)
        ).distinct()

    def by_trip_and_profile(self, trip_id, profile):
        return self.filter(
            trip_id=trip_id
        ).filter(
            models.Q(owner=profile) | models.Q(profiles=profile)
        ).distinct()


class TripAccessTokenManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono czatu o podanym ID")

    def by_token(self, token):
        return self.get(token=token)

