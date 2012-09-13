# Scrapy settings for stella_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import imp, os
from django.core.management import setup_environ

def setup_django_env(path):
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)       
    setup_environ(project)

path = os.environ['VIRTUAL_ENV'] + '/stella_site' 
#setup_django_env('/home/ubuntu/projects/stella/stella_site')
setup_django_env(path)


BOT_NAME = 'stella_crawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['stella_crawler.spiders']
NEWSPIDER_MODULE = 'stella_crawler.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'stella_crawler.pipelines.ItemValidationPipeline',
    'stella_crawler.pipelines.DuplicatesPipeline',
    'stella_crawler.pipelines.DatabasePipeline',
]
