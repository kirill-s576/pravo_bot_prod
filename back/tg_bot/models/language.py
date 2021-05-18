from django.db import models
from django.conf import settings


class Language(models.Model):

    label = models.CharField(max_length=10, choices=settings.LANG_CHOICES)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label}/{self.name}"
