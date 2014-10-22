"""
WSGI config for mcnet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcnet.settings")

sys.path.append('/home/django/mcnet/mcnet')
sys.path.append('/home/django/mcnet')
sys.path.append('/home/django/lib/python2.7/site-packages')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
