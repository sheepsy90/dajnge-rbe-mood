from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from jsonfield import JSONField

from polls.validation import validated_answer_possibilities


class WeeklyQuestion(models.Model):
    """ Weekly questions do not have a correct answer - they are just there for monitoring certain attitudes """
    question = models.CharField(max_length=2048, help_text="The question to ask as a text string")

    answers = JSONField(default={}, help_text="The possible answers stored in a json field")

    pause_seconds = models.IntegerField(default=60*60*24*7, validators=[MinValueValidator(0)],
                                        help_text="Number of seconds until asking this question again")

    active = models.BooleanField(default=False, help_text="Whether the question is actively being asked or not")

    def __str__(self):
        return "Question <id: {}, question: {}>".format(self.id, self.question)

    @property
    def answers_lst(self):
        return sorted(self.answers.items(), key=lambda x: x[1])

    @property
    def answer_count(self):
        return len(self.answers)

    @property
    def validate(self):
        validated_answer_possibilities(self.answers)
        return True

    @staticmethod
    def retrieve_wq_qs_for_user(user):
        """ Retrieves a weekly question if any is available """
        wq_qs1 = WeeklyQuestion.objects.filter(active=True).exclude(weeklyanswer__answered_by=user)
        wq_qs2 = WeeklyQuestion.objects.filter(active=True).filter(weeklyanswer__answered_by=user).exclude(weeklyanswer__answer_again_from__gte=timezone.now())

        wq_qs = wq_qs1 | wq_qs2

        # TODO sqlite cannot do disctince
        id_list = list(set(wq_qs.values_list('id', flat=True)))
        wq_qs = WeeklyQuestion.objects.filter(id__in=id_list)

        return wq_qs


class WeeklyAnswer(models.Model):
    answered_by = models.ForeignKey(User)
    answer = models.IntegerField()
    question = models.ForeignKey(WeeklyQuestion)
    answered_date = models.DateTimeField()
    answer_again_from = models.DateTimeField()

    @staticmethod
    def answer_question(user, answer, question, answered_date):
        assert answer in question.answers.values(), "Answer was not in the given set of accepted values"
        answer_again_from = answered_date + datetime.timedelta(seconds=question.pause_seconds)

        wa = WeeklyAnswer(answered_by=user, answer=answer, question=question, answered_date=answered_date,
                          answer_again_from=answer_again_from)

        wa.save()
        return wa


