from django.db import models


class Message(models.Model):

    label = models.CharField(max_length=24)
    text = models.TextField()

    def __str__(self):
        return self.label

    def get_translation(self, language):
        translations_filter = self.messagetranslate_set.filter(language=language)
        if translations_filter:
            return translations_filter[0].text
        else:
            return self.text
