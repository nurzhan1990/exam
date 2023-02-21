from django import forms
from .models import Questions
from .models import QuestOptions
from django.db import models

CHOICES = (('a','A'), ('b','B'), ('c','C'), ('d','D'))


class QuestionForm(forms.ModelForm):
    # client_approved = forms.MultipleChoiceField(choices=CHOICES)
    client_approved = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # maybe you can set initial with self.fields['my_choices'].initial = initial
        # but it doesn't work wity dynamic choices
        obj = kwargs.get('instance')
        if obj:
            initial = [i for i in obj.client_approved]
            self.initial['client_approved'] = initial
            #print(initial)

    def clean_lead_fields(self):
        return ','.join(self.cleaned_data.get('my_choices', []))

    def clean_client_approved(self):
        # print(self.cleaned_data['client_approved'])
        if len(self.cleaned_data['client_approved']) > 3:
            raise forms.ValidationError('Все варианты не могут быть правильными')
        return self.cleaned_data['client_approved']

    class Meta:
        model = Questions
        fields = ('question_paper','question', 'optionA', 'optionB', 'optionC', 'optionD', 'client_approved')
        # client_approved = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())