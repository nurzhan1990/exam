import ast

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
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
        serializer = CategorySerializer(category, many=True, context={'request': request})
        return Response(serializer.data)


# проверяем, есть ли не законченные тесты у этого пользователя
def check_status(user_id, pk):
    pass_exam_id = PassExam.objects.filter(quest_paper_id=pk, user_id=user_id, status=0)
    if not pass_exam_id:
        exam_data = {'quest_paper': pk, 'user': user_id, 'status': 0}
        serializer = PassExamSerializer(data=exam_data)
        if serializer.is_valid(raise_exception=True):
            pass_exam_id = serializer.save()
    else:
        print(pass_exam_id)
        pass_exam_id = pass_exam_id.first()
    return pass_exam_id


def get_question(pk, pass_exam_id, user_id):
    questions = Questions.objects.filter(question_paper_id=pk)
    question = []
    res = {}
    status = 0
    for item in questions:
        question = item
        status = 0
        pass_exam_list = PassExamList.objects.filter(pass_exam_id=pass_exam_id, question_id=item.id).filter(Q(correct=0) | Q(correct=1))
        if not pass_exam_list:
            pass_exam_list_item = {'question': item.id, 'pass_exam': pass_exam_id, 'user': user_id}
            serializer = PassExamListSerializer(data=pass_exam_list_item)
            if serializer.is_valid(raise_exception=True):
                res['pass_exam_list'] = serializer.save()
                question = item
                status = 1
            break
        else:
            res['pass_exam_list'] = pass_exam_list

    if status == 1:
        res['question'] = Questions.objects.filter(id=question.id)
        return res
    else:
        return False


class QuestionsListView(APIView):

    def get(self, request, pk):
        # uid = self.kwargs['uid']
        user_id = self.request.user.pk
        print('hello')
        pass_exam = check_status(user_id, pk)
        print(pass_exam.id)
        r_quest = get_question(pk, pass_exam.id, user_id)
        print(r_quest)
        serializer = QuestionsSerializer(r_quest['question'], many=True, context={'pass_exam_id': pass_exam.id,'pass_exam_list_id': r_quest['pass_exam_list'].id})
        print('hello3')
        return Response(serializer.data)


class PassExamListCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user_id = self.request.user.pk
        res = check_answer(request.data)
        pel = PassExamList.objects.filter(id=request.data['question']['pass_exam_list_id'])[0]
        if pel:
            pel.correct = res
            pel.answer = request.data['answer']
            pel.save()

        pass_exam_list = PassExamListCreateSerializer(data=request.data['answer'])
        if pass_exam_list.is_valid():
            pass_exam_list.save()

        r_quest = get_question(request.data['question']['question_paper'], request.data['question']['pass_exam_id'], user_id)
        if not r_quest:
            pass_exam = PassExam.objects.filter(id=request.data['question']['pass_exam_id'])[0]
            pass_exam.status = 1
            pass_exam.save()
            return Response({'message':'sucess','code':200}, status=HTTP_200_OK)
        else:
            serializer = QuestionsSerializer(r_quest['question'], many=True, context={'pass_exam_id': request.data['question']['pass_exam_id'], 'pass_exam_list_id': r_quest['pass_exam_list'].id})
            return Response(serializer.data)


def check_answer(dat):
    question = Questions.objects.filter(id=dat['question']['id'])[0]
    answer_true = ast.literal_eval(question.client_approved)
    answer_client = sorted(dat['answer'])
    if answer_true == answer_client:
        return True
    else:
        return False


class CategoryView(ModelViewSet):
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
