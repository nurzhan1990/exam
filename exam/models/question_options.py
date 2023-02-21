from django.db import models
from .question_paper import Question_Paper


class QuestOptions(models.Model):
    choice = models.CharField(max_length=154, unique=True)

    def __str__(self):
        return f' {self.choice}\n'