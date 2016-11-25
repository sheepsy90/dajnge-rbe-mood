from django.conf.urls import include, url
from django.contrib import admin

import polls.views

urlpatterns = [
    # The admin urls and the standard index page url
    url(r'^$', polls.views.landing, name='landing'),
    url(r'^admin/', include(admin.site.urls)),

    # The authorization package for RBE Network
    url(r'^', include('rbe_authorize.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^meta/', polls.views.meta, name='meta'),

]
