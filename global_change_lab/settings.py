"""
Django settings for global_change_lab project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASEDIR = BASE_DIR # for compatibility with django-inlinetrans


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
SITE_ID = 1

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['localhost']
SECRET_KEY = 'localhost-very-secret'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (

    # our own stuff
    'global_change_lab',
    'skills',

    # requirements
    'django.contrib.sites', # requirement for django-allauth

    # django packages
    'south',
    'storages',
    'permission',
    'django_sortable',
    'solo',
    'sortedm2m',
    'embed_video',
    # 'rosetta',
    # 'translations',
    'inlinetrans',
    'django_s3_collectstatic',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # django's own packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # flatpages
    'django.contrib.flatpages',

)

# GZIP security issues
# If you care about HTTPS security, you may want to disable HTTP GZIP compression
# (which is provided by the django gzip middleware)
# See: https://docs.djangoproject.com/en/1.6/ref/middleware/#module-django.middleware.gzip
# Currently we don't use HTTPS so it's not a concern.
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'global_change_lab.urls'

WSGI_APPLICATION = 'global_change_lab.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS += (
    'global_change_lab.context_processors.fatfooter_data',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
    }
}

if os.getenv('GCL_USE_POSTGRES'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'web',
            'HOST': 'localhost',
            'NAME': 'GlobalChangeLab',
            # 'PASSWORD': 'k0Deword.',
        }
    }

STATIC_ROOT = os.path.join(os.getcwd(), 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(os.getcwd(), 'media')
MEDIA_URL = '/media/'

# Sending emails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False # True

USE_TZ = True


# Date (how to display them)
#   in order for these settings to actually take preference `USE_L10N` must be `FALSE`
DATE_FORMAT = 'N jS Y'
DATETIME_FORMAT = 'N jS Y'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# django_extensions
#   enables commands such as `python manage.py show_urls`
if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
    )

# debug_toolbar settings
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
    #    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
    #      'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        # 'debug_toolbar.panels.settings_vars.SettingsVarsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        #'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        # 'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        # 'debug_toolbar.panels.logger.LoggingPanel',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


# General auth
AUTH_USER_MODEL = 'global_change_lab.User'
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin
    "django.contrib.auth.backends.ModelBackend",
)

# django-permissions
AUTHENTICATION_BACKENDS += (
    'permission.backends.PermissionBackend',
)


############################################################
# allauth - BEGIN

DEFAULT_FROM_EMAIL = 'Global Change Lab <hello@globalchangelab.org>'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '' # the default email subject prefix is
                                  # "[{{ site_name }}] " e.g. "[Global Change Lab] "
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # you can login with either
                                                 # username or email
ACCOUNT_SIGNUP_FORM_CLASS = 'global_change_lab.forms.SignupForm'

LOGIN_REDIRECT_URL = 'profile'
LOGIN_URL = '/user/login'

# Sign out immediatly when visiting /account/signout (in this case /user/signout)
# (http://stackoverflow.com/a/18135023/118608)
# (https://django-allauth.readthedocs.org/en/latest/#logout)
# TODO: Change to AJAX POST, since logout on GET is allows 3rd parties to log
#       out the user
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_ADAPTER = 'global_change_lab.allauth.AccountAdapter'

#ACCOUNT_ADAPTER = 'global_change_lab.adapters.AccountAdapter'

TEMPLATE_CONTEXT_PROCESSORS += (
    # allauth specific context processors
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'django.contrib.auth.context_processors.auth',
)
AUTHENTICATION_BACKENDS += (
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# allauth - END
############################################################

# django.contrib.messages
# !!! Messages have been disabled !!!
# Problem: Messages are saved until they are displayed to the user.
#   - As we are not displaying messages right now, they stack indefinitely
#     and seem to have become a performace problem
#
# import django.contrib.messages as messages
# MESSAGE_TAGS = {
#     messages.ERROR: 'alert' # foundation 5 uses 'alert' as its 'error'-class
# }
# INSTALLED_APPS += (
#     'django.contrib.messages',
# )
# TEMPLATE_CONTEXT_PROCESSORS += (
#     'django.contrib.messages.context_processors.messages',
# )
# MIDDLEWARE_CLASSES += (
#     'django.contrib.messages.middleware.MessageMiddleware',
# )

# django-inlinetrans
LOCALE_PATHS = [
    'locale'
]

# django-countries
COUNTRIES_OVERRIDE = {
    '00': ' Other',
}

# Custom middleware - in order to force using English language
# and not e.g. the Danish translation "Dette felt er påkrævet"
#  Note: it must be loaded before the django `LocaleMiddleware`
MIDDLEWARE_CLASSES = (
    'global_change_lab.middleware.ForceDefaultLanguageMiddleware',
) + MIDDLEWARE_CLASSES
