from django.db import models


class Message(models.Model):
    """
    This messages can use like a question into stage.
    Tis messages can use like independent message.
    """
    title = models.CharField(max_length=255, default="Untitled")
    default_text = models.TextField()
    is_hint = models.BooleanField(default=False)

    def __str__(self):
        return self.default_text

    def get_translate(self, language):
        translate_filter = self.messagetranslation_set.filter(language=language)
        if len(translate_filter) > 0:
            return translate_filter.first().text
        else:
            return self.default_text

    def get_translates(self):
        translates = self.messagetranslation_set.all()
        return translates


class StageMessage(models.Model):

    stage = models.ForeignKey("quiz.Stage", on_delete=models.CASCADE)
    message = models.ForeignKey("quiz.Message", on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
