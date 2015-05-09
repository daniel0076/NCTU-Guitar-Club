"""
WSGI config for place_rent project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os,sys
sys.path.append('/home/daniel/virtualenv/django/lib/python3.4/site-packages/')
sys.path.append('/home/daniel/project/place_rent_django/')
sys.path.append('/home/daniel/project/place_rent_django/place_rent/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "place_rent.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
