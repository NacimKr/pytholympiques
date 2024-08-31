"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# application = get_wsgi_application()


#NEW
import os
import sys

# add your project directory to the sys.path
project_home = '/home/nasoooo/pytholympiques'
if project_home not in sys.path:
 sys.path.insert(0, project_home)

os.chdir(project_home)
# set environment variable to tell django where your settings.py is
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

import django
django.setup()

# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
