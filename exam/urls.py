from django.urls import path

from . import views

urlpatterns = [
    path('question_paper/', views.QuestionPaperListView.as_view()),
    path('categories/', views.CategoriesListView.as_view()),
    path('pass_exam/<int:pk>/', views.PassExamListView.as_view(), name='manutencao_os_status'),
]
