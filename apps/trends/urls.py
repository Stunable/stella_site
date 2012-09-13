from django.conf.urls.defaults import *

#from apps.trends.views import trend_notice_modal

urlpatterns = patterns('apps.trends.views',
    url(r'^list/$', 'trend_notice_modal', name='trend_notice_modal'),
    url(r'^delete/(?P<notice_id>\d+)/?$', 'delete_notice', name='trend_delete_notice'),
)