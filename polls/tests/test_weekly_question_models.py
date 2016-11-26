from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from polls.models import WeeklyQuestion, WeeklyAnswer

ANSWERS = {'Yes': 1, 'No': 0}

class TestWeeklyQuestionModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('username', 'email', 'password')
        self.wq = WeeklyQuestion(question="Some sample question?", answers=ANSWERS, pause_seconds=6000, active=True)
        self.wq.save()

    def test_simple_yes_no_question(self):
        self.assertTrue(WeeklyQuestion.objects.all().first().validate)

    def test_answer_generation_for_question_happy_path(self):
        answered_at = timezone.datetime(year=2016, month=11, day=13)
        wa = WeeklyAnswer.answer_question(self.user, 1, self.wq, answered_at)

        self.assertEqual(wa.answer, 1)
        self.assertEqual(wa.question, self.wq)
        self.assertEqual(wa.answered_by, self.user)
        self.assertEqual(wa.answered_date, answered_at)
        self.assertEqual(wa.answer_again_from, answered_at + datetime.timedelta(seconds=6000))

    def test_answer_generation_assertion_raised_on_wrong_answer_value(self):
        answered_at = timezone.datetime(year=2016, month=11, day=13)

        with self.assertRaises(AssertionError) as ae:
            WeeklyAnswer.answer_question(self.user, 'Yes', self.wq, answered_at)

        self.assertEqual(ae.exception.message, 'Answer was not in the given set of accepted values')

    def test_weekly_question_retrieval(self):
        wq_qs = WeeklyQuestion.retrieve_wq_qs_for_user(self.user)

        self.assertEqual(1, wq_qs.count())
        self.assertEqual(self.wq, wq_qs.first())

    def test_weekly_question_retrieval_should_work_after_some_time(self):

        wa = WeeklyAnswer.answer_question(self.user, 1, self.wq, timezone.datetime(year=2015, month=1, day=1))
        wa.save()

        wq_qs = WeeklyQuestion.retrieve_wq_qs_for_user(self.user)
        self.assertEqual(1, wq_qs.count())
        self.assertEqual(self.wq, wq_qs.first())

    def test_weekly_question_retrieval_should_not_work_to_early_after_answer(self):
        answered = timezone.now() - timezone.timedelta(seconds=300)

        wa = WeeklyAnswer.answer_question(self.user, 1, self.wq, answered)
        wa.save()

        wq_qs = WeeklyQuestion.retrieve_wq_qs_for_user(self.user)
        self.assertEqual(0, wq_qs.count())

