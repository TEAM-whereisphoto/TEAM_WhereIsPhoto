"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = get_wsgi_application()
# application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'static'))
# application.add_files(os.path.join(BASE_DIR, 'static'), prefix="more-files/")