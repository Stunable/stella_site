"""The main urls configuration file. Delegates app-specific urls to those
apps' urls confs.
"""

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib.auth import views as auth_views

from beta_invite.forms import SignupForm

admin.autodiscover() # enables admin

# Examples:
# url(r'^$', 'stella_project.views.home', name='home'),
# url(r'^stella_project/', include('stella_project.foo.urls')),

urlpatterns = patterns('',
                       # admin documentation
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # admin
                       url(r'^admin/', include(admin.site.urls)),
                       # Main entry
                       url(r'^$',
                           auth_views.login,
                           {'template_name': 'registration/stella_login.html',
                            'extra_context': {'form_signup': SignupForm()}}),
                       # Beta pages
                       url(r'^beta/', include('beta_invite.urls')),
                       # # user accounts
                       # url(r'^accounts/', include('registration.urls')),
                       # # Main page (Carousel)
                       # url(r'^main/', include('rec.urls')),
                       ## Static pages here on out
                       url(r'^about/$', 
                           direct_to_template,
                           {'template' : 'static/stella_about.html'},
                           name="main-about"),
                       url(r'^contact/$',
                           direct_to_template,
                           {'template': 'static/stella_contact.html'},
                           name="main-contact"),
                       url(r'^thankyou/$',
                           direct_to_template,
                           {'template': 'static/stella_thank-you.html'},
                           name="main-thankyou"),
                       )
