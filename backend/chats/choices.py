from django.db import models

from django.utils.translation import gettext_lazy as _


class ChatroomType(models.TextChoices):
    PRIVATE = 'private', _("Prywatny")
    GROUP = 'group', _("Grupowy")
