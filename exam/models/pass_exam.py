from django.db import models
from .question_paper import Question_Paper
from django.conf import settings


class PassExam(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField()
    quest_paper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quest_paper} '