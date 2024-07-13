# Generated by Django 4.2.13 on 2024-07-13 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_question_teams_remove_user_team_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='news',
        ),
        migrations.RemoveField(
            model_name='teamquestionanswer',
            name='team_answer',
        ),
        migrations.AddField(
            model_name='news',
            name='game',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.game'),
        ),
        migrations.AddField(
            model_name='question',
            name='weight',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='teamquestionanswer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
