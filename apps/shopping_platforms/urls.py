from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
        url(r'^shopify/', include('apps.shopify_app.urls')),
        url(r'^hookup/(?P<API>\w+)$', 'apps.shopping_platforms.views.hookup')

)
