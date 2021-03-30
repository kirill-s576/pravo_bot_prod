from django.db import models


class MessageTranslate(models.Model):

    language = models.ForeignKey("tg_bot.Language", on_delete=models.CASCADE)
    message = models.ForeignKey("tg_bot.Message", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:20]
