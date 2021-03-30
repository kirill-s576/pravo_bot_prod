from django.db import models


class BotUser(models.Model):

    chat_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    language = models.ForeignKey("tg_bot.Language", on_delete=models.SET_NULL, null=True, blank=True)
    memory_message_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name
