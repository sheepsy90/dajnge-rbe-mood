import polls.views

from django.conf.urls import url

urlpatterns = [
    url('index', polls.views.index, name='index'),
    url('refresh_profile', polls.views.refresh_profile, name='refresh_profile')
]
