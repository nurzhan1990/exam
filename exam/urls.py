from django.urls import path

from . import views

urlpatterns = [
    path('question_paper/', views.QuestionPaperListView.as_view()),
    path('categories/', views.CategoriesListView.as_view()),
    path('pass_exam/<int:pk>/', views.QuestionsListView.as_view()),
    path('pass_answer/', views.PassExamListCreateView.as_view()),
    path('UrlForTest/', views.UrlForTest.as_view()),
]
