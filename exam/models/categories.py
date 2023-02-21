from django.db import models
from django.forms import ModelForm


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ExamForm(ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'
