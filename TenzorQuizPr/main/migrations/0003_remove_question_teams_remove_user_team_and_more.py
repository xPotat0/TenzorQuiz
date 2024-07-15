# Generated by Django 4.2.13 on 2024-07-12 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_game_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='user',
            name='team',
        ),
        migrations.AddField(
            model_name='teamquestionanswer',
            name='game',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.game'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
    ]