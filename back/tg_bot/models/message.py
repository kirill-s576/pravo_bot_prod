from django.db import models


class Message(models.Model):

    label = models.CharField(max_length=24)
    text = models.TextField()

    def __str__(self):
        return self.label

    @property
    def translates(self):
        return self.messagetranslate_set.all()

    def get_translate_by_language_id(self, language_id):
        return self.translates.get(language_id=language_id)


    def get_translation(self, language):
        translations_filter = self.messagetranslate_set.filter(language=language)
        if translations_filter:
            return translations_filter[0].text
        else:
            return self.text

    @classmethod
    def get_message_by_translate_text(cls, translate_text):
        filtered_objects = cls.objects.filter(text=translate_text)
        if len(filtered_objects) > 0:
            return filtered_objects.first()
        else:
            filtered_objects = cls.objects.filter(messagetranslate__text=translate_text)
            if len(filtered_objects) > 0:
                return filtered_objects.first()
            else:
                return None
