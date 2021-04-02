from django.db import models
import json


class BotUser(models.Model):

    chat_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    language = models.ForeignKey("tg_bot.Language", on_delete=models.SET_NULL, null=True, blank=True)
    memory_message_id = models.CharField(max_length=255)
    _memory = models.TextField(default="{}")

    def __str__(self):
        return self.user_name

    @property
    def messages_memory(self):
        return json.loads(self._memory)

    @messages_memory.setter
    def messages_memory(self, value):
        self._memory = json.dumps(value)