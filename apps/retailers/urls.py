from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template,redirect_to
from retailers.views import *
from contact_form.views import contact


urlpatterns = patterns('',
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
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
    url(r'^wepay', setup_wepay),
    url(r'^$', redirect_to, {'url':'/accounts/login'}, name="home"),
    url(r'^notification/', include('apps.notification.urls')),
    url(r'^racks/', include('apps.racks.urls')),
    url(r'^shop/', include('apps.racks.urls')),
     
    url(r'^trends/', include('apps.trends.urls')),
    url(r'^blog/', include('apps.blog.urls')),
    url(r'^news/', include('apps.news.urls'))

)
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='main-about'),
    url(r'^faq/$', 'flatpage', {'url': '/faq/'}, name='faq'),
    url(r'^team/$', 'flatpage', {'url': '/team/'}, name='team'),
    url(r'^return/$', 'flatpage', {'url': '/return/'}, name='return'),
    url(r'^careers/$', 'flatpage', {'url': '/careers/'}, name='careers'),
    url(r'^we_love_developers/$', 'flatpage', {'url': '/we_love_developers/'}, name='devs'),
    url(r'^how_it_works/$', 'flatpage', {'url': '/how_it_works/'}, name='hiw'),
    url(r'^privacy/$', 'flatpage', {'url': '/privacy/'}, name="main-privacy"),
    url(r'^terms/$', 'flatpage', {'url': '/terms/'}, name="terms"),
)

urlpatterns += patterns('',
     url(r'^$',
        'contact_form.views.contact',name='main-contact'),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.ADMIN_MEDIA_ROOT,
        }),
        
   )

