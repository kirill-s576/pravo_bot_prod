from django.db import models
import json
from typing import List
from django.utils import timezone
from django.core.exceptions import ValidationError
from json.decoder import JSONDecodeError


USER_INTERFACE_CHOICES = [
    ("site", "Site"),
    ("telegram", "Telegram")
]


class SessionManager(models.Manager):

    def filter_for_last(self, minutes: int):
        if not minutes:
            return self.all()
        now = timezone.now()
        delta = timezone.timedelta(minutes=minutes)
        since = now - delta
        return self.filter(created_at__gt=since)


def steps_json_validator(value):
    try:
        steps_list = json.loads(value)
        if type(steps_list) is not list:
            raise ValidationError("Steps must be list")
    except JSONDecodeError:
        raise ValidationError("Steps must be JSON convertible string")


class Session(models.Model):

    user_id = models.CharField(max_length=255)
    user_from = models.CharField(max_length=255, choices=USER_INTERFACE_CHOICES)
    language = models.ForeignKey("quiz.Language", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    finished = models.BooleanField(default=False)

    _steps = models.TextField(default="[]", blank=True)

    objects = SessionManager()

    @property
    def steps(self) -> List[int]:
        return json.loads(self._steps)

    @steps.setter
    def steps(self, value: List[int]) -> None:
        self._steps = json.dumps(value)

    def add_step(self, stage_id: int) -> None:
        local_steps = self.steps
        local_steps.append(stage_id)
        self.steps = local_steps
        self.save()

    def pop_step(self) -> int:
        local_steps = self.steps
        step = local_steps.pop()
        self.steps = local_steps
        self.save()
        return step

    def clear_steps(self) -> None:
        self.steps = []
        self.save()
