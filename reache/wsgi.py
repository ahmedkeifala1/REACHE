"""
WSGI config for reache project.

It exposes the WSGI callable as a module-level variable named ``application``.
Vercel's Python runtime looks for one named ``app``, so both are defined here.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reache.settings')

application = get_wsgi_application()

# Django stops serving MEDIA_ROOT once DEBUG is off (see reache/urls.py), and on
# Vercel there is no web server in front of the application to take over. The
# WhiteNoise middleware only covers STATIC_ROOT, so the uploaded photography is
# added here instead.
from django.conf import settings  # noqa: E402  (must follow get_wsgi_application)

if settings.MEDIA_ROOT.exists():
    from whitenoise import WhiteNoise

    application = WhiteNoise(application)
    application.add_files(str(settings.MEDIA_ROOT), prefix=settings.MEDIA_URL)

app = application
