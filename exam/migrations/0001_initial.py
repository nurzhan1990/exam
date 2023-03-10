# Generated by Django 4.1.7 on 2023-02-16 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PassExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Question_Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.categories')),
            ],
        ),
        migrations.CreateModel(
            name='QuestOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=154, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100)),
                ('optionA', models.CharField(max_length=100)),
                ('optionB', models.CharField(max_length=100)),
                ('optionC', models.CharField(max_length=100)),
                ('optionD', models.CharField(max_length=100)),
                ('client_approved', models.CharField(default=list, max_length=100)),
                ('question_paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.question_paper')),
            ],
        ),
        migrations.CreateModel(
            name='PassExamList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=100)),
                ('correct', models.IntegerField()),
                ('pass_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.passexam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='passexam',
            name='quest_paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.question_paper'),
        ),
        migrations.AddField(
            model_name='passexam',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
