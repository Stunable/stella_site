from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from apps.accounts.views import *
from django.contrib.auth import views as auth_views

from forms import LoginForm
from accounts.views import add_facebook_friend


urlpatterns = patterns('',
    url(r'^profile$', profile_edit ,name='profile_edit'),
    url(r'^check_login/$', check_login ,name='check_login'),

    url(r'^avatar/upload', avatar_upload, name='avatar_upload'),
    url(r'^logout$',
       auth_views.logout,
       {'next_page': '/',
        'template_name': 'rec/main.html'},
       name='logout'),
    url(r'^connect', connect, name="connect")

)


# django-registration urls

urlpatterns += patterns('registration.views',
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        'activate',
        name='registration_activate'),
    url(r'^register/$',
        'register',
        name='registration_register'),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
)


# Standard django.contrib.auth.views
urlpatterns += patterns('django.contrib.auth.views',
    # For redirecting back
    url(r'^login/$',
        'login',
        {'template_name': 'registration/login.html',
         'authentication_form': LoginForm },
        name='auth_login'),
    url(r'^logout/$',
        'logout_then_login',
#       {'template_name': 'registration/logout.html'},
        name='auth_logout'),
)





