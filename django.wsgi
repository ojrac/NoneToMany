import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.insert(0, '/usr/share/hubspot/webapps/eliza')

# This has to be done here otherwise Django won't be in a directory
# that's in PYTHONPATH.
from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
