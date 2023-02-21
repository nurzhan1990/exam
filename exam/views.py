from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from exam.models import Questions
from exam.models.pass_exam import PassExam
from exam.models.pass_exam_list import PassExamList
from exam.serializers import *
from exam.models.categories import Categories
from exam.models.question_paper import Question_Paper


class QuestionPaperListView(APIView):

    def get(self, request):
        question_papers = Question_Paper.objects.all()
        serializer = QuestionPaperSerializer(question_papers, many=True)
        return Response(serializer.data)


class CategoriesListView(APIView):

    def get(self, request):
        category = Categories.objects.all()
        serializer = CategorySerializer(category, many=True,context={'request': request})
        return Response(serializer.data)


class PassExamListView(APIView):

    def get(self, request, pk):
        # uid = self.kwargs['uid']
        user_id = self.request.user.pk
        cat_id = PassExam.objects.filter(quest_paper_id=pk, user_id=user_id)
        if not cat_id:
            exam_data = {'quest_paper': pk, 'user': self.request.user.pk, 'status': 0}
            serializer = PassExamSerializer(data=exam_data)
            if serializer.is_valid(raise_exception=True):
                cat_id = serializer.save()
        print(cat_id)
        return Response(cat_id)


class CategoryView(ModelViewSet):
    print('asdasdasda')
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class QuestionPaperView(ModelViewSet):
    serializer_class = QuestionPaperSerializer

    def get_queryset(self):
        uid = self.kwargs['uid']
        print(uid)
        queryset = Question_Paper.objects.filter(category_id_id=uid)
        return queryset


class QuestionsView(ModelViewSet):
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        uid = self.kwargs['uid']


        exam_data = {}
        # exam_data['author'] = request.user.id  # setting the user as author
        exam_data['quest_paper'] = uid
        # print(self.request.user.pk)
        exam_data['user'] = self.request.user.pk
        serializer = PassExamSerializer(data=exam_data)
        if serializer.is_valid(raise_exception=True):
            res = serializer.save()



            res1 = Questions.objects.filter(category_id_id=uid)
            serializer_class = PassExamSerializer
            queryset2 = PassExam.objects.select_related('quest_paper')

            r_questions = PassExamList.objects.select_related('question')
                # .values_list('question__question','question__optionA','question__optionB')

            # r_questions = Questions.objects.select_related('qu')
            print(str(r_questions.query))
            print(r_questions)
        # Actor.objects.filter(followers__country__name='Bulgaria', followers__group__title='Sportists')

        # for item in queryset:
        #     exam_data_list = {}
        #     exam_data_list['pass_exam'] = uid
        #     exam_data_list['question'] = item.pk
        #     exam_data_list['correct'] = 1
        #     exam_data_list['user'] = self.request.user.pk
        #
        #     serializer = PassExamListSerializer(data=exam_data_list)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()

        queryset3 = Questions.objects.all()

        return r_questions


def index_main(reuqest):
    return render(reuqest, 'main/index.html')