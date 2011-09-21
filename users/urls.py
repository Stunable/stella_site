"""Specific urls for the users side of things. 
"""

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^login/$', auth_views.login, 
                           template_name="main.html"),
                       url(r'^logout/$', auth_views.logout,
                           template_name="main.html"),
)
