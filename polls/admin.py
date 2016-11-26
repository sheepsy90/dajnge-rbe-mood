from django.contrib import admin

from polls.models import WeeklyAnswer, WeeklyQuestion

admin.site.register(WeeklyAnswer)
admin.site.register(WeeklyQuestion)
