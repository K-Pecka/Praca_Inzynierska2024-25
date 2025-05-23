from django.db import models

from dicts.models import BaseModel
from users.models import CustomUser


class Order(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_type = models.CharField(max_length=50, blank=True, null=True)
