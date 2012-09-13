from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from api.handlers import ProductHandler, RetailerHandler, InventoryHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

product_resource = Resource(handler=ProductHandler, **ad)
retailer_resource = Resource(handler=RetailerHandler, **ad)
inventory_resource = Resource(handler=InventoryHandler, **ad)

urlpatterns = patterns('',
    url(r'^retailer/$', retailer_resource),
    url(r'^product/$', product_resource), 
    url(r'^product/(?P<pk>\d+)/$', product_resource),
    url(r'^product/(?P<pk>\d+)/(?P<inventory>\w+)/$', product_resource),
    url(r'^inventory/$', inventory_resource),
    url(r'^inventory/(?P<pk>\d+)/$', inventory_resource),
)