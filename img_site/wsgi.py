"""
WSGI config for img_site project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import os.path
import sys

sys.path.append(r'/Library/Python/2.7/site-packages/')
sys.path.append(r'/srv/img_site')

os.environ['DJANGO_SETTINGS_MODULE'] = 'img_site.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#application = django.core.handlers.wsgi.WSGIHandler()
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)