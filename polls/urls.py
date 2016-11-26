import polls.views

from django.conf.urls import url

urlpatterns = [
    url('index', polls.views.index, name='index'),
    url('question_types', polls.views.question_types, name='question_types'),
    url('settings_page', polls.views.settings_page, name='settings_page'),

    url('answer_weekly_question', polls.views.answer_weekly_question, name='answer_weekly_question'),
    url('weekly_question', polls.views.weekly_question, name='weekly_question'),
    url('specific_survey', polls.views.specific_survey, name='specific_survey'),
]
