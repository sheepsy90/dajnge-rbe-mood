import polls.views

from django.conf.urls import url

urlpatterns = [
    url('index', polls.views.index, name='index'),
    url('question_types', polls.views.question_types, name='question_types'),
    url('settings_page', polls.views.settings_page, name='settings_page'),
]
