from django.conf.urls.defaults import *
from apps.retailers.views import create_shipping_label,view_shipping_label,print_packing_slip


urlpatterns = patterns('cart.views',
    url(r'^buy_rack/(?P<rack_id>\d+)$',
        view='buy_rack',
        name='buy_rack'
    ), 
    url(r'^add_to_cart/(?P<product_id>\d+)/(?P<quantity>\d+)/(?P<size>.*)$',
        view='add_to_cart',
        name='add_to_cart'
    ),                  
    url(r'^update_cart/(?P<product_id>\d+)/?$',
        view='update_cart',
        name='update_cart'
    ),
    url(r'^remove_from_cart/(?P<product_id>\d+)/$',
        view='remove_from_cart',
        name='remove_from_cart'
    ),
    url(r'^$',
        view='get_cart',
        name='get_cart'
    ),
    url(r'^update_info',
        view='update_info',
        name='update_cart_info'
    ),                 
    url(r'^validate_address',
        view='validate_address',
        name='validate_address'
    ),   
    url(r'^validate_cc',
        view='validate_cc',
        name='validate_cc'
    ),                 
    url(r'^order_history',
        view='order_history',
        name='order_history'
    ),
    url(r'^update_zipcode',
        view='update_zipcode',
        name='update_zipcode'
    ),
    url(r'^shopper_return_purchase',
        view='shopper_return_purchase',
        name='shopper_return_purchase'
    ),
    url(r'^shopper_return_item',
        view='shopper_return_item',
        name='shopper_return_item'
    ),                       
    url(r'^shopper_request_refund_item',
        view='shopper_request_refund_item',
        name='shopper_request_refund_item'
    ),                       
    url(r'^details$',
        view='wpp',
        name='express_checkout'
    ),
    url(r'^order_placed$',
        view='place_order',
        name='place_order'
    ),
    url(r'^success',
        view='wpp_success',
        name='wpp_success'
    ),
    url(r'^wpp_reference_pay',
        view='wpp_reference_pay',
        name='wpp_reference_pay'
    ),
    url(r'^print_shipping_label/(?P<ref>\w+)', create_shipping_label, name='user_print_shipping_label'),
    url(r'^view_shipping_label/(?P<shipping_number>\w+)', view_shipping_label, name='user_view_shipping_label'),
    url(r'^print_packing_slip/(?P<shipping_number>\w+)',print_packing_slip, name='user_print_packing_slip'),

)
