from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import Questions
from .pass_exam import PassExam
from django.conf import settings


class PassExamList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pass_exam = models.ForeignKey(PassExam, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question_papers")
    answer = models.CharField(max_length=100,blank=True)
    correct = models.IntegerField(default=3,
        validators=[
            MaxValueValidator(2),
            MinValueValidator(1)
        ],blank=True)

    def __str__(self):
        return f'{self.pass_exam} '