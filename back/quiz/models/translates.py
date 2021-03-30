from django.db import models


class MessageTranslation(models.Model):

    language = models.ForeignKey('quiz.Language', on_delete=models.CASCADE)
    message = models.ForeignKey('quiz.Message', on_delete=models.CASCADE)
    text = models.TextField()


class QButtonTranslation(models.Model):

    language = models.ForeignKey('quiz.Language', on_delete=models.CASCADE)
    button = models.ForeignKey('quiz.QButton', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)