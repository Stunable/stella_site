from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
        url(r'^$', 'apps.stunable_shopify.views.index', name='shopify_root_path'),
        url(r'^design/$', 'apps.stunable_shopify.views.design'),
        url(r'^welcome/$', 'apps.stunable_shopify.views.welcome'),
)
