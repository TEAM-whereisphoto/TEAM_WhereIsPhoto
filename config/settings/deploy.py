from .base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

# WSGI application
WSGI_APPLICATION = 'config.wsgi.deploy.application'