"""
These are settings specific to the staging environment. 

 - DEBUG is still on
 - DB is specific to staging env
 - CACHE_BACKEND 
 - EMAIL_HOST and EMAIL_PORT might change once more intricate staging occurs
 - SITE_ID
 - The global logging level (via logging.root.setLevel())

"""

from base_settings import *

# The DB should mimic the one we will end up using 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_stella_staging',
        'USER': 'pg_stella',
        'PASSWORD': '123shockchewy123',
        'HOST': '',
        }
}

TEMPLATE_DIRS = (
    "/var/www/shopwithstella.com/dev/stella_root/stella_project/templates",
)
