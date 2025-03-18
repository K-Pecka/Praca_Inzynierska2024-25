from django.db import models

from django.utils.translation import gettext_lazy as _

from chats.choices import ChatroomType
from chats.managers import ChatroomManager, ChatMessageManager
from dicts.models import BaseModel
from users.models import UserProfile
from trips.models import Trip


class Chatroom(BaseModel):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )
    type = models.CharField(
        max_length=32,
        choices=ChatroomType.choices,
        default=ChatroomType.PRIVATE,
        verbose_name=_("Typ"), help_text=_("Typ")
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.PROTECT,
        related_name="chat_rooms",
        verbose_name=_("Wycieczka"), help_text=_("Wycieczka")
    )
    creator = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="chat_rooms_creator",
        verbose_name=_("Przewodnik"), help_text=_("Przewodnik")
    )
    members = models.ManyToManyField(
        UserProfile,
        related_name="chat_rooms",
        blank=True,
        verbose_name=_("Turysta"), help_text=_("Turyści")
    )
    settings = models.JSONField(
        default=dict,
        verbose_name=_("Ustawienia"), help_text=_("Ustawienia")
    )

    objects = ChatroomManager()

    def clean(self):
        if not self.pk:
            self.save()

    class Meta:
        db_table = "chat_rooms"
        verbose_name = "Pokój do czatowania"
        verbose_name_plural = "Pokoje do czatowania"
        ordering = ["-created_at"]


class ChatMessage(BaseModel):
    text = models.TextField(
        max_length=512,
        verbose_name=_("Nazwa"), help_text=_("Nazwa")
    )
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="chat_messages",
        verbose_name=_("Autor wiadomości"), help_text=_("Autor wiadomości")
    )
    file = models.FileField(
        upload_to="chat_files/",
        blank=True, null=True,
        verbose_name=_("Plik"), help_text=_("Plik")
    )
    chatroom = models.ForeignKey(
        Chatroom,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name=_("Pokój do czatowania"), help_text=_("Pokój do czatowania")
    )

    objects = ChatMessageManager()

    class Meta:
        db_table = "chat_messages"
        verbose_name = "Wiadomość czatu"
        verbose_name_plural = "Wiadomości czatu"
        ordering = ["-created_at"]
