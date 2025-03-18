from django.db import models
from django.db.models import Q

from rest_framework.exceptions import NotFound


class ChatroomManager(models.Manager):
    def by_id(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono czatu o podanym ID")

    def by_user(self, profile):
        return self.filter(Q(creator=profile) | Q(members=profile)).distinct()


class ChatMessageManager(models.Manager):
    def by_chatroom_pk(self, room_pk):
        try:
            return self.get(chatroom=room_pk)
        except self.model.DoesNotExist:
            raise NotFound(detail="Nie znaleziono wiadomości o podanym ID")

    def by_user_and_chatroom(self, profile, room_pk):
        return self.filter(profile=profile, chatroom=room_pk)
