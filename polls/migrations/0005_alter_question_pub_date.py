# Generated by Django 4.2.5 on 2023-09-09 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_question_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
