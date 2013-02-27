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
    ('Dev Alerts', 'gdamon@gmail.com'),
    ('More Dev Alerts', 'admin@stunable.com'),
)

CONTACT_LIST = (
   ('Dev Alerts', 'gdamon@gmail.com'),
   ('More Dev Alerts', 'admin@stunable.com'),
)


RETAILER_EMAIL = 'stylists@stunable.com'


SHOPIFY_API_KEY = "a9dca1e81ac8554c181100b5a47de622"
SHOPIFY_API_SECRET = "bc1b2b77901a3d1cd0ec408eb33fe315"
# See http://api.shopify.com/authentication.html for available scopes
# to determine the permisssions your app will need.
SHOPIFY_API_SCOPE = ['read_products', 'read_orders', 'write_products' 
]

AWS_ACCESS_KEY_ID = "AKIAJX3OAPMY5SVE2KHA"
AWS_SECRET_ACCESS_KEY ="WjtqEmMuuK3sqrg7G5+4q9Hpo+CjeSepvA2urEQw"
USE_AMAZON_S3 = True
AWS_STORAGE_BUCKET_NAME = "images.stunable.com"
AWS_S3_CUSTOM_DOMAIN = 'images.stunable.com'
DEFAULT_BUCKET = "images.stunable.com"
AWS_S3_SECURE_URLS = False

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_HEADERS = {
    'Cache-Control': 'max-age=186400000',
}


THUMB_SIZES = {'tiny':(90,90), 'small':(150,300),'medium':(200,400),'large':(700,700),'extralarge':(1280,1280)}

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

ADMIN_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/admin-media')

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

INITIAL_RACKS = ['A Night Out on the Town', "A day at the Beach"]


SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0


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
    # 'sslify.middleware.SSLifyMiddleware',
    # 'johnny.middleware.LocalStoreClearMiddleware',
    # 'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'apps.common.middleware.ProfileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'shopify_app.middleware.LoginProtection',
)

JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_st'
# some johnny settings
# CACHES = {
#     'default' : dict(
#         BACKEND = 'johnny.backends.redis.RedisCache',
#         LOCATION = '127.0.0.1:6379',
#         JOHNNY_CACHE = True,
#     )
# }

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

SOUTH_TESTS_MIGRATE = False # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True # To disable South's own unit tests

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
    'django.contrib.sitemaps',    
    'accounts',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    #'registration',
    #'beta_invite',
    'massadmin',
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
    # 'paypal',
    'cart',
    'contact_form',
    'bootstrap',
    'sorl.thumbnail',
    'ckeditor',
    'registration',
    'openpyxl',
    # 'paypal.standard',
    # 'paypal.pro',
    'stunable_wepay',
    'api',
    'gunicorn',
    'stunable_shopify',
    'shopify_app',
    #'chronograph'
    #'kombu.transport.django',
    'djcelery',
    'storages',
    'queued_storage',
)

BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
BROKER_HOST = "127.0.0.1" # this will be our master server IP
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"

import djcelery
CELERY_IMPORTS = (
    'apps.retailers',
    'apps.racks',
    'apps.cms'
)

CELERYBEAT_SCHEDULER = 'edjcelery.schedulers.DatabaseScheduler'
djcelery.setup_loader()

# django-registration
ACCOUNT_ACTIVATION_DAYS = 14
LOGIN_REDIRECT_URL = "/accounts/connect"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s.%(funcName)s line: %(lineno)d : %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
        ,
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'stunable_debug':{
            'handlers': ['console'],
            'level': 'DEBUG',
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
    "apps.common.context_processors.page_role",
    "django.core.context_processors.request",
    "apps.cms.context_processors.CMS",
    'shopify_app.context_processors.current_shop',
    'django.core.context_processors.debug'
    )


INTERNAL_IPS = ('127.0.0.1',)


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
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
# FACEBOOK_SCOPE = 'publish_stream'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'apps.social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
    'apps.accounts.backends.EmailAuthenticationBackend',
)

SOCIAL_AUTH_ENABLE_BACKENDS = ('facebook', 'google','twitter')
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


WEPAY_FIXED_FEE = .30
WEPAY_PERCENTAGE = 2.9

ITEM_RETURN_LIMIT = 14#days

PAYPAL_MECHANT_ACCOUNT_ID ='VR92K8L7B4U7U'
TAX_RATE = 0.1

STELLA_DEFAULT_EMAIL = "Stunable"

WAITLIST_ACTIVE = True

NOTICE_TIME_DIFF = 2 #minutes


THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_DEBUG = True

EXTERNAL_CONTENT_URL = {
                            'blog':"http://stunable.wordpress.com/",
                            'news': "http://stunablenews.wordpress.com/"
                        }

TAX_USE_TAXCLOUD = True
TAX_USE_TAXCLOUD_AUTHORIZATION = True
TAX_TAXCLOUD_API_ID = '15B54040'
TAX_TAXCLOUD_API_KEY = '0D678AA9-B974-44AF-B1E5-6DB714D26E55'
USPS_ID = '193BURLE8091'


try:                        
    from dev import *
except:
    from prod import *

