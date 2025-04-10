from django.db import models


class ActivePermissionsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def by_name(self, code):
        return self.filter(code=code).distinct()
