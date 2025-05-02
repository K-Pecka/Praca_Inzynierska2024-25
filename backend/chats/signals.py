from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from chats.models import Chatroom
from trips.models import Trip
from chats.choices import ChatroomType
from django.db.models import Q

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


@receiver(post_save, sender=Trip)
def create_private_chatrooms_for_trip_members(sender, instance, created, **kwargs):
    """Tworzymy prywatne pokoje czatowe pomiędzy przewodnikiem a każdym uczestnikiem wycieczki"""
    if created:
        members = instance.members.all()

        for member in members:
            if member != instance.creator:  # Ignorujemy czat pomiędzy przewodnikiem a samym sobą
                chatroom = Chatroom.objects.create(
                    name=f"Czat: {instance.creator.user.first_name} & {member.user.first_name}",
                    type=ChatroomType.PRIVATE,
                    trip=instance,
                    creator=instance.creator,
                )
                chatroom.members.add(instance.creator, member)


@receiver(m2m_changed, sender=Trip.members.through)
def sync_chatroom_members_on_trip_members_update(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for member_id in pk_set:
            try:
                member = instance.members.get(id=member_id)
            except instance.members.model.DoesNotExist:
                continue

            if member != instance.creator:
                chatroom = Chatroom.objects.create(
                    name=f"Czat: {instance.creator.user.first_name} & {member.user.first_name}",
                    type=ChatroomType.PRIVATE,
                    trip=instance,
                    creator=instance.creator,
                )
                chatroom.members.add(instance.creator, member)

    elif action == 'post_remove':  # Usunięcie członka
        for member_id in pk_set:
            try:
                member = instance.members.get(id=member_id)
                chatroom = Chatroom.objects.filter(
                    trip=instance,
                    type=ChatroomType.PRIVATE
                ).filter(
                    Q(members=instance.creator) & Q(members=member)
                ).first()
                if chatroom:
                    chatroom.delete()  # Usuwamy czat
            except instance.members.model.DoesNotExist:
                continue
