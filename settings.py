import os, sys
# Django settings for stella_project project.

IS_DEV = False
IS_PROD = True

# Get the ENV setting. Needs to be set in .bashrc or similar.
# export ENV='dev' or export ENV='prod'

#ENV = os.getenv('ENV')
ENV="dev"
if not ENV:
    raise Exception('Environment variable ENV is requried!')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

ADMINS = (
    ('Dev Alerts', 'dev-alerts@simpleunion.com'),
)

CONTACT_LIST = (
    ('Dev Alerts', 'dev-alerts@simpleunion.com'),
    ('Stella Admin', 'admin@shopwithstella.com'),
)

MANAGERS = ADMINS

# project root and add "apps" to the path
PROJECT_ROOT = os.path.abspath(os.path.split(__file__)[0])
APPS_ROOT = os.path.join(PROJECT_ROOT, 'apps')
sys.path.append(APPS_ROOT)
 
# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'NOREPLY@STUNABLE.COM'
EMAIL_HOST_PASSWORD = 'Numba1!!'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

ADMIN_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/admin-media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

ADMIN_MEDIA_URL = '/media/admin-media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, '_static')


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' # URL prefix for admin static files -- CSS, JavaScript and images.  # Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'sdlkjldjh(*&sdfj2398JHsdfn89&9sdfhjk2h12309usnfklsdnf*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'longerusername',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.markup',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.flatpages',    
    'accounts',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    #'registration',
    #'beta_invite',
    'south',
    'friends',
    'notification',
    'cms',
    'racks',
    'trends',
    'voting',
    'tagging',
    'stella_crawler',
    'blog',
    'inlines',
    'news',
    'social_auth',
    'retailers',
    'paypal',
    'cart',
    'contact_form',
    'bootstrap',
    'sorl.thumbnail',
    'ckeditor',
    'registration',
    'openpyxl',
    'paypal.standard',
    'paypal.pro',
    'api',
    'gunicorn',
    'chronograph'
)

# django-registration
ACCOUNT_ACTIVATION_DAYS = 14
LOGIN_REDIRECT_URL = "/accounts/login/"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "apps.notification.context_processors.notification",
    "apps.trends.context_processors.trend_count",
    "apps.friends.context_processors.friend_notice_count",
    "racks.context_processors.racks",
    "django.core.context_processors.request",)


SITE_NAME = "STELLA"
CONTACT_EMAIL = "stella@shopwithstella.com"

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# default rack
DEFAULT_RACK = 5

# days of absenses
ABSENT_DAYS = 7 

CKEDITOR_UPLOAD_PATH = MEDIA_ROOT

FACEBOOK_APP_ID = "397462356974539"
FACEBOOK_SECRET_KEY = "bdea442bf0c2113602662f7632939d73"
FACEBOOK_SCOPE = 'publish_stream'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
    'apps.accounts.backends.EmailAuthenticationBackend',
)

SOCIAL_AUTH_ENABLE_BACKENDS = ('facebook', 'twitter')
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

PRODUCT_GROUPS = {
    'product_group_a': (0, 60),
    'product_group_b': (60,110),
    'product_group_c': (110, 200),
    'product_group_d': (200, 320),
    'product_group_e': (320, sys.maxint)
}


PAYPAL_TEST = True           # Testing mode on
PAYPAL_WPP_USER = "thanh_1346909527_biz_api1.simpleunion.com"      # Get from PayPal
PAYPAL_WPP_PASSWORD = "1346909592"
PAYPAL_WPP_SIGNATURE = "AuNpYqzF97TLkPdB7Ifqg4fv0yT4ADn0-4ImkElljllTI3S6XkW26Hy3"
PAYPAL_RECEIVER_EMAIL = "thanh_1346909527_biz@simpleunion.com"


PAYPAL_MECHANT_ACCOUNT_ID ='VR92K8L7B4U7U'
TAX_RATE = 0.1

STELLA_DEFAULT_EMAIL = "Stunable"

WAITLIST_ACTIVE = True

NOTICE_TIME_DIFF = 2 #minutes

FACEBOOK_EXTENDED_PERMISSIONS = ['publish_stream, email']

EXTERNAL_CONTENT_URL = {
                            'blog':"http://stunable.wordpress.com/",
                            'news': "http://stunablenews.wordpress.com/"
                        }
                        
from dev import *

