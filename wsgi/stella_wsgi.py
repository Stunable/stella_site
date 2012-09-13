SITE_DIR = '/var/projects/stella/stella_site'
import site, os, sys
site.addsitedir(SITE_DIR)
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

