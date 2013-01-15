from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from retailers.views import *

urlpatterns = patterns('',
    url(r'^create_profile$', create_retailer_profile, name='create_retailer_profile'),
    url(r'^update_profile$', update_retailer_profile, name='update_retailer_profile'),
    url(r'^shopify/', include('apps.shopify_app.urls')),
    url(r'^product_list$', product_list, name='product_list'),
    url(r'^info/(?P<name>\w+)?', retailer_information, name='retailer_information'),
    url(r'^item/bulk_upload/(?P<upload_id>\d+)?$', bulk_upload, name='bulk_upload'),
    url(r'^item/add$', add_item, name='add_item'),
    url(r'^item/delete/(?P<item_id>\d+)', delete_item, name='delete_item'),
    url(r'^item/edit/(?P<item_id>\d+)', edit_item, name='edit_item'),
    url(r'^(?P<retailer_id>\d+)/view_all_products', view_all_products, name='view_all_products'),
    url(r'^upload_logo$', retailer_logo_upload, name='retailer_logo_upload'),
    url(r'^list$', retailer_list, name='retailer_list'),
    url(r'^retailer_modal/(?P<item_id>\d+)$', retailer_modal, name='retailer_modal'),
    url(r'^order_history', order_history, name='retailer_order_history'),
    url(r'^help', retailer_help, name='retailer_help'),
    url(r'^(?P<retailer_id>\d+)/terms$', terms, name='retailer_terms'),
    url(r'^(?P<retailer_id>\d+)/terms_complete$', terms_complete, name='retailer_terms_complete'),
    url(r'^order/update/(?P<order_item_id>\d+)', update_order_item, name='retailer_update_order_item'),
    url(r'^print_shipping_label/(?P<ref>\w+)', create_shipping_label, name='print_shipping_label'),
    url(r'^view_shipping_label/(?P<shipping_number>\w+)', view_shipping_label, name='view_shipping_label'),
    url(r'^print_packing_slip/(?P<shipping_number>\w+)',print_packing_slip, name='print_packing_slip'),
    url(r'^item_action', item_action),
    url(r'^wepay', setup_wepay)
)

