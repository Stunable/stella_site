
print "USING PROD SETTINGS"
# dev overrides
DEBUG = False
IS_DEV = False
IS_PROD = True
SSL_ENABLED = False
# COMPRESS = True   # to test django compressor locally

# domains/hosts etc.
DOMAIN_NAME = 'stunable.com'
WWW_ROOT = 'https://%s/' % DOMAIN_NAME

FACEBOOK_APP_ID              = '396733507047008'
FACEBOOK_API_SECRET          = '642be492d594607d661a6517b5529050'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

GOOGLE_OAUTH2_CLIENT_SECRET = 'XEFZ7iOvh6gxmiEwEof_p4JI'
GOOGLE_OAUTH2_CLIENT_ID = '79164646909.apps.googleusercontent.com'
GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.google.com/m8/feeds','https://www.googleapis.com/auth/plus.me']

TWITTER_CONSUMER_KEY = 'Fl9NGVMMdhpT2OTOKj9pvw'
TWITTER_CONSUMER_SECRET = '6YCE4XTamJXgjBXunWYMMgpqMo4Oj0chCiNvt3758'


WEPAY_ACCESS_TOKEN = "94e911521e8f645d2a40a4370d179b10c4483dc15fc87b9be55d3230de40fcd5"
WEPAY_CLIENT_ID = "76739"
WEPAY_ACCOUNT_ID = "1941411742"
WEPAY_CLIENT_SECRET = "cf356f0e63"
WEPAY_PRODUCTION = True
WEPAY_STAGE = "production"

SHOPIFY_API_KEY = "0bccd168c35ce06f12af9ce75d9adeb9"
SHOPIFY_API_SECRET = "e87147b636bad9a76512700306407ba5"
# See http://api.shopify.com/authentication.html for available scopes
# to determine the permisssions your app will need.
SHOPIFY_API_SCOPE = ['read_products', 'read_orders', 'write_products' 
]


LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/accounts/connect/'
LOGIN_ERROR_URL = '/login/'

SOCIAL_AUTH_ENABLE_BACKENDS = ('facebook','google-oauth2','twitter')
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

#registration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stunable',                      
        'USER': 'stunable',
        'PASSWORD': 'stunable!',
        'HOST': ''
    }
}


THUMBNAIL_DEBUG = True

# sandbox
PAYPAL_URL = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'
PAYPAL_PDT_URL = 'https://www.sandbox.paypal.com/au/cgi-bin/webscr'


WAITLIST_ACTIVE = False 
THUMBNAIL_DEBUG = False

from fedex.config import FedexConfig

# Change these values to match your testing account/meter number.
######PROD
FEDEX_CONFIG = FedexConfig(key='zA9Z6uz3gHNKkU3L',
                         password='8TA1Z49ZTJztPJ8a6uPqsjqKF',
                         account_number='147593830',
                         meter_number='104573181',
                         use_test_server=False)


####DEV
# FEDEX_CONFIG = FedexConfig(key='G9zxZissGIQkOgo4',
#                          password='bX3GkoY0uIQjrIl1m66jT2OTa',
#                          account_number='510087968',
#                          meter_number='118562345',
#                          use_test_server=True)


PAYPAL_TEST = True           # Testing mode on
PAYPAL_WPP_USER = "thanh_1346909527_biz_api1.simpleunion.com"      # Get from PayPal
PAYPAL_WPP_PASSWORD = "1346909592"
PAYPAL_WPP_SIGNATURE = "AuNpYqzF97TLkPdB7Ifqg4fv0yT4ADn0-4ImkElljllTI3S6XkW26Hy3"
PAYPAL_RECEIVER_EMAIL = "thanh_1346909527_biz@simpleunion.com"


# add local_settings.py to override this file
try:
    from local_settings import *
except ImportError, exp:
    print 'bad import of local settings'
    pass
