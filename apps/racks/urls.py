from django.conf.urls.defaults import *
from apps.racks.views import *
from apps.racks.views import _all

urlpatterns = patterns('',
                       url(r'^add_size', add_size, name="add_size"),
                       url(r'^add_color', add_color, name="add_color"),
                       url(r'^detail/(?P<rack_id>\d+)', detail, name="racks_detail"),
                       url(r'^carousel/stella_choice', stella_choice, name="stella_choice"),
                       url(r'^carousel/all', _all, name='all'),
                       url(r'^carousel/new', new, name='new'),
#                       url(r'^carousel/change_it_up', change_it_up, name="change_it_up"),
                       url(r'^carousel/(?P<category_id>\w+)', carousel, name="carousel"),
                       url(r'^sent_to_admirer/', send_item_to_admirer, name="send_item_to_admirer"),
                       url(r'^add_item/', add_item_from_modal, name="add_item_from_modal"),
                       url(r'^$', index, name="racks_index"),
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
                       url(r'^item$', item, name='item'),
                       url(r'^item/show_modal/(?P<item_id>\d+)', item_modal, name='item_modal'),
                       url(r'^jean_submit/', jean_submit, name='jean_submit'),
                       #url(r'^item_add/(?P<rack_id>\d+)', rack_item_add, name="rack_item_add"),
                       #url(r'^item_add_new/(?P<rack_id>\d+)', rack_item_add_new, name="rack_item_add_new"),
                       url(r'search', search, name='rack_search'),
                       url(r'brands', get_brands, name='get_brands'),  
                       
                       url(r'sale', sale_items, name='my_closet_sale_items'),
                       url(r'recent_added', recent_added_items, name='my_closet_recent_added_items'),
                       url(r'purchased', purchased_items, name='my_closet_purchased_items'),
                       url(r'^trendsetters/(?P<user_id>\d+)$', trendsetters, name='trendsetters'),
                       url(r'^steal/(?P<rack_id>\d+)/$', steal_rack, name='steal_rack'),
                       url(r'^get_new_notifications/$', get_new_notifications, name='get_new_notifications'),
                       url(r'^display_notice_table/$', display_notice_table, name='display_notice_table'),
                       )