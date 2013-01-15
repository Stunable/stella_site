from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
        url(r'^$', 'shopify_app.views.login'),
        url(r'^authenticate/$', 'apps.shopify_app.views.authenticate'),
        url(r'^finalize/$', 'apps.shopify_app.views.finalize'),
        url(r'^logout/$', 'apps.shopify_app.views.logout'),
        url(r'^load$', 'apps.shopify_app.views.load', name='shopify_root_path'),
)
