"""
Django settings for global_change_lab project under mocha test conditions.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from .settings import *
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/gcl-messages' # change this to a proper location
ALLOWED_HOSTS += ( 'kh.vpn.bitblueprint.com' )
DEBUG = True

