from django.conf.urls.defaults import *
from apps.friends.views import invite, search, delete, accept_join, index, decline_invitation, accept_invitation, invite_modal, add
from friends.views import get_friends,query_friends,fb_add

urlpatterns = patterns('',
                       url(r'^$', index, name="friend_index"),
                       url(r'invite', invite, name='friend_invite'),
                       url(r'invite_modal', invite_modal, name='invite_modal'),
                       url(r'^query_friends/(?P<q>)?',query_friends, name='query_friends'),
                       url(r'search', search, name='friend_search'),
                       url(r'add/(?P<user_id>\d+)', add, name='friend_add'),
                       url(r'addfb/(?P<user_id>\d+)', fb_add, name='fb_friend_add'),
                       url(r'delete/(?P<user_id>\d+)', delete, name='friend_delete'),
                       url(r'accept_join/(?P<confirmation_key>\w+)', accept_join, name='friend_accept_join'),
                       url(r'accept_invitation/(?P<sender_id>\w+)/(?P<notification_id>\d+)', accept_invitation , name='accept_invitation'),
                       url(r'decline_invitation/(?P<sender_id>\w+)/(?P<notification_id>\d+)', decline_invitation , name='decline_invitation'),
                       url(r'get_friends', get_friends, name="get_friends"),
                       )