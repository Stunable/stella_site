from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
        url(r'^$', 'apps.shopify_app.views.login'),
        url(r'^authenticate/$', 'apps.shopify_app.views.authenticate'),
        url(r'^finalize/$', 'apps.shopify_app.views.finalize'),
        url(r'^logout/$', 'apps.shopify_app.views.logout'),
)
