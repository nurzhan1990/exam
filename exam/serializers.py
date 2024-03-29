from django.forms import CharField
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from exam.models import Categories, Question_Paper, Questions
from exam.models.pass_exam import PassExam
from exam.models.pass_exam_list import PassExamList


class QuestionPaperSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    continue_exam = CharField()

    class Meta:
        model = Question_Paper
        fields = "__all__"

    #добавляем поле статус чтобы знать, продолжить тест или новый начать
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = self.context["request"].user.id
        cat_id = PassExam.objects.filter(quest_paper_id=data['id'], user_id=user_id).order_by('-id')[:1]
        print(cat_id)
        if cat_id:
            data["status"] = cat_id.values_list("status", flat=True)[0]
        else:
            data["status"] = False
        return data


class CategorySerializer(ModelSerializer):
    question_papers = QuestionPaperSerializer(many=True)

    class Meta:
        model = Categories
        fields = "__all__"


class QuestionsSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["pass_exam_id"] = self.context["pass_exam_id"]
        data["pass_exam_list_id"] = self.context["pass_exam_list_id"]
        return data

    class Meta:
        model = Questions
        exclude = ('client_approved',)


class PassExamSerializer(ModelSerializer):
    class Meta:
        model = PassExam
        fields = ['id', 'user', 'quest_paper', 'status']


class PassExamListSerializer(ModelSerializer):
    class Meta:
        model = PassExamList
        fields = ['id', 'pass_exam', 'question', 'correct', 'user']


class PassExamListCreateSerializer(ModelSerializer):
    class Meta:
        model = PassExamList
        fields = ['id', 'pass_exam', 'question', 'correct', 'user']


class PassExamListCountSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["client_approved"] = data['question']['client_approved']
        return data

    class Meta:
        model = PassExamList
        depth = 1
        exclude = ('user','pass_exam',)