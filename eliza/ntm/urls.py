from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'eliza.ntm.views.index'),
    (r'^ask/(?P<conversation_uuid>[-a-zA-Z0-9]{36})/?$', 'eliza.ntm.views.ask'),
)

