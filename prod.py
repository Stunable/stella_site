
# dev overrides
DEBUG = False
IS_DEV = False
IS_PROD = True
SSL_ENABLED = False
# COMPRESS = True   # to test django compressor locally

# domains/hosts etc.
DOMAIN_NAME = 'localhost:7777'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME

FACEBOOK_APP_ID              = '397462356974539'
FACEBOOK_API_SECRET          = 'bdea442bf0c2113602662f7632939d73'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/add_facebook_friend/'
LOGIN_ERROR_URL = '/login/'

SOCIAL_AUTH_ENABLE_BACKENDS = ('facebook')
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

#registration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stella',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '123456',
        'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
        }
    }
}

THUMBNAIL_DEBUG = True

# sandbox
PAYPAL_URL = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'
PAYPAL_PDT_URL = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'


WAITLIST_ACTIVE = True 
THUMBNAIL_DEBUG = False

from apps.cart.plugins.fedex.config import FedexConfig

# Change these values to match your testing account/meter number.
# Change these values to match your testing account/meter number.
FEDEX_CONFIG = FedexConfig(key='G9zxZissGIQkOgo4',
                         password='bX3GkoY0uIQjrIl1m66jT2OTa',
                         account_number='510087968',
                         meter_number='118562345',
                         use_test_server=True)

PAYPAL_TEST = True           # Testing mode on
PAYPAL_WPP_USER = "thanh_1346909527_biz_api1.simpleunion.com"      # Get from PayPal
PAYPAL_WPP_PASSWORD = "1346909592"
PAYPAL_WPP_SIGNATURE = "AuNpYqzF97TLkPdB7Ifqg4fv0yT4ADn0-4ImkElljllTI3S6XkW26Hy3"
PAYPAL_RECEIVER_EMAIL = "thanh_1346909527_biz@simpleunion.com"


# add local_settings.py to override this file
try:
    from local_settings import *
except ImportError, exp:
    pass
