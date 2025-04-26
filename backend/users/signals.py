from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserProfile, UserProfileType, get_or_create_default_user_profile_type


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when a new user is created.
    """
    if created:
        if not instance.is_guest:
            default_type = get_or_create_default_user_profile_type()
            UserProfile.objects.create(user=instance, type=default_type, is_default=True)
        else:
            guest_type, created = UserProfileType.objects.get_or_create(code='guest', name='Gosc')
            UserProfile.objects.create(user=instance, type=guest_type, is_default=True)

