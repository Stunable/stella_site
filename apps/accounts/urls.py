from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from apps.accounts.views import *
from django.contrib.auth import views as auth_views

from forms import LoginForm
from accounts.views import add_facebook_friend


urlpatterns = patterns('',
    url(r'^profile$', profile_edit ,name='profile_edit'),
    url(r'^update_profile$', update_profile, name='update_profile'),
    url(r'^create_new_shipping_info', create_new_shipping_info, name='create_new_shipping_info'),
    url(r'^(?P<info_id>\d+)/update_shipping_info', update_shipping_info, name='update_shipping_info'),
    url(r'^(?P<info_id>\d+)/make_default', make_default, name="make_default"),
    url(r'^cc/set_default/(?P<id>\d+)/', cc_set_default, name='cc_set_default'),
    url(r'^update_answers$', update_answers, name='account_update_answers'),
    url(r'^create/complete$',
         direct_to_template,
         {'template': 'accounts/account_create_confirm.html'},
         name = 'create_confirm'),
    url(r'^avatar/upload', avatar_upload, name='avatar_upload'),
    url(r'^logout$',
       auth_views.logout,
       {'next_page': '/',
        'template_name': 'rec/main.html'},
       name='logout'),
    url(r'^welcome$', welcome, name="welcome"),
    url(r'^invite_waitlist/$',
        invite_waitlist,
        name='invite_waitlist'),
    url(r'^new_user_join/(?P<confirmation_key>\w+)', new_user_join, name='new_user_join'),
    url(r'^connect', connect, name="connect"),
    url(r'^add_facebook_friend', add_facebook_friend, name="add_facebook_friend")
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
    url(r'^password/change/$',
        'password_change',
        name='auth_password_change'),
    url(r'^password/change/done/$',
        'password_change_done',
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        'password_reset',
        {'template_name': 'registration/password_reset_form.html'},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm',
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        'password_reset_complete',
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        'password_reset_done',
        name='auth_password_reset_done'),
)


if settings.WAITLIST_ACTIVE:
    urlpatterns += patterns('',
        url(r'^invite_waitlist', invite_waitlist, name='account_create'),
        url(r'^login_with_fb$', invite_waitlist, name='login_with_fb'),
        url(r'^create$', invite_waitlist),
    )
else:
    urlpatterns += patterns('',
        url(r'^create$', create, name='account_create'),
        url(r'^login_with_fb$', login_with_fb, name='login_with_fb'),
    )


