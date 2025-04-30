from django.db.models.signals import post_save
from django.dispatch import receiver
from chats.models import Chatroom
from trips.models import Trip
from chats.choices import ChatroomType


@receiver(post_save, sender=Trip)
def create_announcement_chatroom(sender, instance, created, **kwargs):
    if created:
        Chatroom.objects.create(
            name=f"Ogłoszenia – {instance.name}",
            type=ChatroomType.GROUP,  # albo 'announcement' jeśli masz osobny typ
            trip=instance,
            creator=instance.creator,
        )
