
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stunable',                      
        'USER': 'stunable',
        'PASSWORD': 'stunable!',
        'HOST': ''
    }
}

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

CACHE_MIDDLEWARE_SECONDS = 60

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/accounts/connect/'
LOGIN_ERROR_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DOMAIN_NAME = "%(live_host)s"
WWW_ROOT = 'https://%(live_host)s/'

DEBUG = "%(mode)s" is "dev"
