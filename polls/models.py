import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    A template model representing questions.

    Methods:
        __str__: Returns the text of the question model.
        was_published_recently: Returns a boolean indicating whether this poll question is currently published or not.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date suppressed', null=True, default=None)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        now = timezone.now()
        if self.end_date is None:
            return self.is_published()
        return self.is_published() and now < self.end_date


class Choice(models.Model):
    """
    A template model representing choices.

    Returns:
        __str__: Returns the text of the choices model.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text