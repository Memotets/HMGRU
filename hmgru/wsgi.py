"""
WSGI config for hmgru project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from hmgru.AutocallController import AutocallController

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmgru.settings')

application = get_wsgi_application()

controller = AutocallController()
controller.initThread()
