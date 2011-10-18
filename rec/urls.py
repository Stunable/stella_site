""" The recommendation urls configuration file. 
"""

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                       # Main rec page
                       url(r'^$', 
                           direct_to_template,
                           {'template': 'rec/main.html'}),
                       )
