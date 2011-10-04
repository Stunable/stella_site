"""Specific urls for the users side of things. 
"""

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       (r'^login/$', auth_views.login, 
                        {'template_name': 'accounts/login.html'}),

                       (r'^logout/$', auth_views.logout,
                        {'template_name': 'accounts/logged_out.html'}),

                       (r'^password_change/$', auth_views.password_change,
                        {'template_name': 'accounts/password_change_form.html'}),

                       (r'^password_change/done/$', auth_views.password_change_done,
                        {'template_name': 'accounts/password_change_done.html'}),
)
