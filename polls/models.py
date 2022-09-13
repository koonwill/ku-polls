""" Model for Polls Application"""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Model for Poll Question."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def __str__(self):
        """str -- Poll Question text."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',)
    def was_published_recently(self):
        """Check that question is published less than 1 day or not
        return True if question was published less than 1 day, False otherwise.
        """
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """return True if current date is on or after question’s publication date."""
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        """check user in the voting period or not then 
        return True if voting is allowed for this question.
        """
        now = timezone.localtime()
        if self.end_date == None:
            return self.pub_date <= now
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Model for choice in Polls."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """str -- Poll choice text."""
        return self.choice_text
