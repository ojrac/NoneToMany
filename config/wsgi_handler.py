import os
import site
import sys
paths = ('/usr/share/hubspot/webapps/eliza')
for path in paths:
    if path not in sys.path:
        sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'eliza.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
