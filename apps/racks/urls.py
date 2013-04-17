from django.conf.urls.defaults import *
from apps.racks.views import *
from apps.racks.views import _all

urlpatterns = patterns('',
                       url(r'^add_size', add_size, name="add_size"),
                       url(r'^add_color', add_color, name="add_color"),

                       
                       url(r'^daily/(?P<slug>[-\w]+)', daily, name="daily"),
                       url(r'^friends', friends, name='friends'),

                       # url(r'^tab/(?P<slug>[-\w]+)', carousel, name="tagged_carousel"),                     
                      
                       
                       url(r'^remove-tab/(?P<slug>[-\w]+)', tab_handler, {'method': 'remove'}, name="remove_tab"),
                       url(r'^add-tab/(?P<slug>[-\w]+)?', tab_handler, {'method': 'add'}, name="add_tab"),

                       url(r'^$', carousel, name="all"),

                       url(r'^wishlist_item/(?P<wishlist_item_id>[-\w]+)?', variation_modal, name='variation_modal'),
                       url(r'^wishlist', wishlist, name='wishlist'),

                       url(r'^new', new, name='new'),
                       url(r'^all', _all, {'all_items':True}, name='all'),
                       url(r'^sale', sale_items, name='sale'),

                       # these can be direct linked
                       url(r'^item/(?P<slug>[-\w]+)', item_modal, name='item_modal'),
                       url(r'^brand/(?P<slug>[-\w]+)', stylist, name="stylist"),
                       url(r'(?P<group>[-\w]+)/(?P<slug>[-\w]+)',flavor,name="flavor")

                       )
