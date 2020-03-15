"""
WSGI config for po_fp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if not bool(os.environ.get("DEBUG", default=False)):
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "po_fp.settings")

application = get_wsgi_application()
if not bool(os.environ.get("DEBUG", default=False)):
    application = Sentry(application)
