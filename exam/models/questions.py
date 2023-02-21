from django.db import models
from .question_paper import Question_Paper
from .question_options import QuestOptions


APPROVAL_CHOICES = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
)

class Questions(models.Model):
    question_paper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100)
    optionD = models.CharField(max_length=100)
    client_approved = models.CharField(max_length=100, default=list)
    # client_approved = models.ManyToManyField(QuestOptions)

    def __str__(self):
        return f'{self.question} {self.optionA}'

