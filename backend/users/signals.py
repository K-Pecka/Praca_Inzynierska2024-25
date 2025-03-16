from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_guest:
            UserProfile.objects.create(user=instance, is_default=True)
        else:
            UserProfile.objects.create(user=instance, type='guest')

