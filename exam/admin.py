from django.contrib import admin
from .models import *
from .forms import QuestionForm
from .models.pass_exam import PassExam
from .models.pass_exam_list import PassExamList

admin.site.register(Categories)
admin.site.register(Question_Paper)
admin.site.register(QuestOptions)
admin.site.register(PassExam)
admin.site.register(PassExamList)
# admin.site.register(Questions)
#
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm

admin.site.register(Questions, QuestionAdmin)