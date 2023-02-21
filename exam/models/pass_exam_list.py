from django.db import models

from . import Questions
from .pass_exam import PassExam
from django.conf import settings


class PassExamList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pass_exam = models.ForeignKey(PassExam, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    correct = models.IntegerField()

    def __str__(self):
        return f'{self.pass_exam} '