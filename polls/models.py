import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """
    A template model representing questions.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date suppressed', null=True,
                                    default=None, blank=True)

    def __str__(self):
        """Return the text of the question"""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return True if the poll was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return True if the poll is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return True if the poll is in the voting period."""
        now = timezone.now()
        if self.end_date is None:
            return self.is_published()
        return self.is_published() and now < self.end_date


class Choice(models.Model):
    """
    A template model representing choices.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """count the votes for this choice."""
        # choice = Vote.objects.filter(choice=self).count()
        return self.vote_set.count()

    def __str__(self):
        """Return text of the choice"""
        return self.choice_text


class Vote(models.Model):
    """Records a Vote of a Choice by User."""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)