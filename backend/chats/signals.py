from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from chats.models import Chatroom
from trips.models import Trip
from chats.choices import ChatroomType


@receiver(post_save, sender=Trip)
def create_announcement_chatroom(sender, instance, created, **kwargs):
    if created:
        chatroom = Chatroom.objects.create(
            name=f"Ogłoszenia – {instance.name}",
            type=ChatroomType.GROUP,
            trip=instance,
            creator=instance.creator,
        )
        chatroom.members.set(instance.members.all())


@receiver(m2m_changed, sender=Trip.members.through)
def sync_chatroom_members_on_trip_members_update(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        try:
            chatroom = Chatroom.objects.get(trip=instance, type=ChatroomType.GROUP)
        except Chatroom.DoesNotExist:
            return
        chatroom.members.add(*pk_set)
