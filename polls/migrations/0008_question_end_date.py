# Generated by Django 4.2.5 on 2023-09-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_remove_question_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=None, verbose_name='date suppressed'),
            preserve_default=False,
        ),
    ]
