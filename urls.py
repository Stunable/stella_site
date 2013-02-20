"""The main urls configuration file. Delegates app-specific urls to those
apps' urls confs.
"""

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin
from django.contrib.auth import views as auth_views

from apps.beta_invite.forms import SignupForm
from django.core.urlresolvers import reverse
from voting.views import vote_on_object
from django.views.generic.list_detail import object_list
from racks.models import Item
from racks.views import carousel 
from django.shortcuts import redirect


from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

items = {
    'queryset': Item.objects.all(),
    'date_field': 'created_date',
}

on_sale = {
    'queryset': Item.objects.filter(is_onsale=True),
    'date_field': 'created_date',
}


sitemaps = {
    'flatpages': FlatPageSitemap,
    'items': GenericSitemap(items, priority=0.6),
    'items_on_sale':GenericSitemap(on_sale, priority=0.666),
}

admin.autodiscover() # enables admin


urlpatterns = patterns('',
                       url(r'^$', 
                           'apps.racks.views.gethome',
                           name="home"),
                       url(r'', include('social_auth.urls')),
                       url(r'^registration/', include('apps.registration.urls')),
                       url(r'^login/$', redirect_to, {'url': '/login/facebook'}),
                       url(r'^admin/cmstest/', 'apps.cms.views.text_test'),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # export a model to csv
                       (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'common.views.admin_list_export'),
                       (r'^admin/', include("massadmin.urls")),                       
                       url(r'^admin/', include(admin.site.urls)),
                       # Beta pages
                       url(r'^beta/', include('beta_invite.urls')),
                       ## Static pages here on out
                       url(r'^help$', 
                           direct_to_template,
                           {'template' : 'static/stella_help.html'},
                           name="main-help"),
                       url(r'^contact/', include('contact_form.urls')),                       
                       url(r'^thankyou/$',
                           direct_to_template,
                           {'template': 'static/stella_thank-you.html'},
                           name="main-thankyou"),
#                       url(r'^privacy/$',
#                           direct_to_template,
#                           {'template': 'static/privacy-policy.html'},
#                           name="main-privacy"),
#                       url(r'^terms/$',
#                           direct_to_template,
#                           {'template': 'static/terms_of_service.html'},
#                           name="terms"),              
                       url(r'^accounts/', include('apps.accounts.urls')),
                       url(r'^admirers/', include('apps.friends.urls')),
                       url(r'^notification/', include('apps.notification.urls')),
                      
                       url(r'^shop/', include('apps.racks.urls')),
                        # url(r'^racks/', include('apps.racks.urls')),
                       url(r'^trends/', include('apps.trends.urls')),
                       
                       url(r'^vote/?$', object_list, dict(queryset=Item.objects.all(),
                            template_object_name='link', template_name='racks/item_vote_list.html',
                            paginate_by=15, allow_empty=True)),
                            
                       # item vote
                       url(r'^item_vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
                            vote_on_object, dict(model=Item, template_object_name='Item',
                                template_name='racks/vote_on_item.html',
                                post_vote_redirect='/',
                                allow_xmlhttprequest=True),
                           name="item_vote"),
                       
                       # blog apps
                       url(r'^comments/', include('django.contrib.comments.urls')),
                       url(r'^news/', include('news.urls')),
                       url(r'^blog/', include('blog.urls')),
                       
                       # facebook integration
                       url(r'^facebook/', include('facebook.urls')),
                        
                       # retailer app
                       url(r'^retailers/', include('retailers.urls')),
                    
                       url(r'^cart/', include('cart.urls')),
                       
                       (r'^ckeditor/', include('ckeditor.urls')),
                       (r'^api/', include('api.urls')),
                      
                       (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
                       # # paypal integration app
                       # (r'^purchased/(?P<uid>\d+)/(?P<id>\d+)/$', 'paypal.views.purchased' ), # purchase callback

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

    
    
