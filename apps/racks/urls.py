from django.conf.urls.defaults import *
from apps.racks.views import *
from apps.racks.views import _all

urlpatterns = patterns('',
                       url(r'^add_size', add_size, name="add_size"),
                       url(r'^add_color', add_color, name="add_color"),
                       url(r'^detail/(?P<rack_id>\d+)', detail, name="racks_detail"),
                       url(r'^carousel/stella_choice', stella_choice, name="stella_choice"),
                       url(r'^all', _all, {'all_items':True}, name='all'),
                       url(r'^new', new, name='new'),

                       url(r'^stylist/(?P<stylist_id>\d+)', stylist, name="stylist"),



#                       url(r'^carousel/change_it_up', change_it_up, name="change_it_up"),
                       url(r'^trendsetters/(?P<user_id>\d+)?$', trendsetters, name='trendsetters'),


                       url(r'^tab/(?P<slug>[-\w]+)', carousel, name="tagged_carousel"),
                       url(r'^flavor/(?P<slug>[-\w]+)', flavor, name="tagged_carousel"),
                       url(r'^item/(?P<item_slug>[-\w]+)', item_modal, name='item_modal'),

                       url(r'^remove-tab/(?P<slug>[-\w]+)', tab_handler, {'method': 'remove'}, name="remove_tab"),
                       url(r'^add-tab/(?P<slug>[-\w]+)?', tab_handler, {'method': 'add'}, name="add_tab"),



                       url(r'^sent_to_admirer/', send_item_to_admirer, name="send_item_to_admirer"),
                       url(r'^add_item/', add_item_from_modal, name="add_item_from_modal"),
                       url(r'^$', index, name="all"),
                       url(r'^shared', shared, name='list_shared_racks'),
                       url(r'^public', public, name='list_public_racks'),
                       url(r'^delete/(?P<rack_id>\d+)', delete, name="rack_delete"),
                       url(r'^edit/(?P<rack_id>\d+)', edit, name="rack_edit"),
                       url(r'^update_rack_name/(?P<rack_id>\d+)', update_rack_name, name="update_rack_name"),
                       url(r'^share/(?P<rack_id>\d+)', share, name="rack_share"),
                       url(r'^share_modal/(?P<rack_id>\d+)', share_modal_view, name="share_modal_view"),
#                       url(r'^item_delete/(?P<rack_id>\d+)/(?P<rack_item_id>\d+)', rack_item_delete, name="rack_item_delete"),
                       url(r'^item_remove/(?P<rack_id>\d+)/(?P<rack_item_id>\d+)', rack_item_remove, name="rack_item_remove"),
                       url(r'^add$', add, name='racks_add'),
                       url(r'^add_admirer/(?P<rack_id>\d+)/(?P<friend_id>\d+)', add_admirer, name="add_admirer"),
                       url(r'^remove_admirer/(?P<rack_id>\d+)/(?P<friend_id>\d+)', remove_admirer, name="remove_admirer"),
                       # url(r'^item$', item, name='item'),
                       
                       url(r'^wishlist_item/(?P<wishlist_item_id>[-\w]+)?', variation_modal, name='variation_modal'),

                       url(r'^wishlist', wishlist, name='wishlist'),
                       url(r'^friends', friends, name='friends'),
                       url(r'^jean_submit/', jean_submit, name='jean_submit'),
                       
                       
                       url(r'sale', sale_items, name='sale'),

                       url(r'^display_notice_table/$', display_notice_table, name='display_notice_table'),
                       )
