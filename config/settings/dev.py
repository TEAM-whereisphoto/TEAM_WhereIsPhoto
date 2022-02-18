from .base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

config_secret_dev = json.loads(open(CONFIG_SECRET_DEV_FILE).read())

ALLOWED_HOSTS = config_secret_dev['django']['allowed_hosts']

# WSGI application
WSGI_APPLICATION = 'config.wsgi.dev.application'