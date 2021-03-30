from django.db import models


class QButton(models.Model):
    """

    """
    default_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.default_text

    def get_translate(self, language):
        translate_filter = self.qbuttontranslation_set.filter(language=language)
        if len(translate_filter) > 0:
            return translate_filter.first().text
        else:
            return self.default_text
    
    def get_translates(self):
        translates = self.qbuttontranslation_set.all()
        return translates
