# Generated by Django 4.2.13 on 2024-07-17 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('gender', models.BooleanField(default=None, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('role', models.IntegerField(choices=[(0, 'Участник'), (1, 'Ведущий')], default=0)),
                ('login', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
