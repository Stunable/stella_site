from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import shopify
from decorators import shop_login_required

from racks.models import Item,ItemType,Color,Size,ProductImage
from retailers.models import ShopifyProduct,ShopifyVariation,ShopifyConnection,StylistItem,RetailerProfile,get_retailer_profile
from apps.shopping_platforms.tasks import *


from django.contrib.auth import authenticate

from django.contrib.auth import login as django_login

import logging
logger = logging.getLogger('stunable_debug')

from django.db import transaction


from django.core.files import File
import urllib

import pprint

import tempfile
import os


PP = pprint.PrettyPrinter(indent=4)

def _return_address(request):
    return request.session.get('return_to') or reverse('shopify_root_path')

def login(request):
    # Ask user for their ${shop}.myshopify.com address

    # If the ${shop}.myshopify.com address is already provided in the URL,
    # just skip to authenticate
    if request.REQUEST.get('shop'):
        return authenticate(request)
    return render_to_response('shopify_app/login.html', {},
                              context_instance=RequestContext(request))

def authenticate(request):
    shop = request.REQUEST.get('shop')
    if shop:
        scope = settings.SHOPIFY_API_SCOPE
        permission_url = shopify.Session.create_permission_url(shop.strip(), scope)
        return redirect(permission_url)

    return redirect(_return_address(request))

def finalize(request):
    shop_url = request.REQUEST.get('shop')
    try:
        shopify_session = shopify.Session(shop_url, request.REQUEST)
    except:
        # messages.error(request, "Could not log in to Shopify store.")
        return authenticate(request)

    request.session['shopify'] = {
                "shop_url": shop_url,
                "access_token": shopify_session.token
            }
    # messages.info(request, "Logged in to shopify store.")

    response = redirect(_return_address(request))
    request.session.pop('return_to', None)
    return response

def logout(request):
    request.session.pop('shopify', None)
    # messages.info(request, "Successfully logged out.")

    return redirect(reverse('shopify_app.views.login'))

@shop_login_required
def load(request,APICONNECTION=ShopifyConnection,ITEM_API_CLASS=ShopifyProduct,VARIATION_API_CLASS= ShopifyVariation):
    retailer_profile = get_retailer_profile(request)

    shopify_connection = None

    if not retailer_profile:#we don't have a logged in retailer
        try:
            #check and see if there is already a retailer profile with shopify connection that matches this shop url
            #if so, it means we can login the user associated with that shopify account
            shopify_connection = APICONNECTION.objects.filter(shop_url=request.session['shopify']['shop_url'])[0] 
            redirect_url = reverse("product_list")

            retailer_profile = shopify_connection.retailer_profile

            logger.info('shopify found existing retailer profile:%s'%str(retailer_profile))

            # at this point we attempt to login the profile's user which may or may not exist and therefore might fail...
            user = retailer_profile.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, user)

            update_API_products.delay(shopify_connection)
            return redirect(redirect_url) 
        except Exception, e:
            logger.info('shopify retailer profile/user not found/error:'+str(e))
            pass #continue setting up this new shopify connection

    # if we're still here it's because we couldn't log in a user from a retailer profile associated with an authenticated shopify store
    redirect_url = reverse("create_retailer_profile")

    
    if retailer_profile:
        pass
        # if we have retailer profile at this point but did not get a user above,
        # it's because one was created with this connection but the profile is incomplete
        # we will redirect to the profile creation page to complete the info, but we do not need a new profile
    else:
        retailer_profile = RetailerProfile.objects.create()
        
    if not shopify_connection:
        shopify_connection,created = APICONNECTION.objects.get_or_create(retailer_profile=retailer_profile,shop_url=request.session['shopify']['shop_url'])

    request.session['active_api_connection'] = shopify_connection
    request.session['active_retailer_profile'] = retailer_profile

    shopify_connection.access_token = request.session['shopify']['access_token']
    shopify_connection.update_in_progress = True
    shopify_connection.save()
    update_API_products.delay(shopify_connection)
    return redirect(redirect_url)


