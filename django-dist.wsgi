import os, sys
sys.path.append('YOUR-ROOT-DIRECTORY-ABOVE-DJANGO-APPLICATION')
sys.path.append('YOUR-ROOT-DIRECTORY-ABOVE-DJANGO-APPLICATION/YOUR-APPLICATION-NAME')
os.environ['DJANGO_SETTINGS_MODULE'] = 'YOUR-APPLICATION-NAME.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
