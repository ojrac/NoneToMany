from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'eliza.ntm.views.index'),
    (r'^ask$', 'eliza.ntm.views.ask'),
)

