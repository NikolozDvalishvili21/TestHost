# Generated by Django 5.0.6 on 2024-08-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_remove_quiz_answers_remove_quiz_num_answers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='answer1_is_correct',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='answer2_is_correct',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='answer3_is_correct',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='answer4_is_correct',
        ),
        migrations.AddField(
            model_name='quiz',
            name='correct_answer',
            field=models.IntegerField(choices=[(1, 'Answer 1'), (2, 'Answer 2'), (3, 'Answer 3'), (4, 'Answer 4')], null=True, verbose_name='Correct Answer'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='question',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
