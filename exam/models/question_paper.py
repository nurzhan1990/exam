from django.db import models
from .categories import Categories


class Question_Paper(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="question_papers")

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category_id else 'No Parent'})"
