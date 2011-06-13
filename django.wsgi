import os, sys
sys.path.append('/homes/cs390cp')
sys.path.append('/homes/cs390cp/icypc-ladder')
os.environ['DJANGO_SETTINGS_MODULE'] = 'icypc-ladder.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
