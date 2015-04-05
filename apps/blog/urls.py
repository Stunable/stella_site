from django.conf.urls.defaults import *


urlpatterns = patterns('apps.blog.views',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view='post_list',
        name='blog_detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        view='post_list',
        name='blog_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        view='post_list',
        name='blog_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        view='post_list',
        name='blog_archive_year'
    ),
    url(r'^categories/(?P<slug>[-\w]+)/$',
        view='post_list',
        name='blog_category_detail'
    ),
    url (r'^categories/$',
        view='post_list',
        name='blog_category_list'
    ),
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view='post_list',
        name='blog_tag_detail'
    ),
    url (r'^search/$',
        view='post_list',
        name='blog_search'
    ),
    url(r'^page/(?P<page>\d+)/$',
        view='post_list',
        name='blog_index_paginated'
    ),
    url(r'^$',
        view='post_list',
        name='blog_index'
    ),
)
