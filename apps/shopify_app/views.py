from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import shopify
from decorators import shop_login_required

from racks.models import Item,ItemType,Color,Size,ProductImage
from retailers.models import ShopifyProduct,ShopifyVariation,ShopifyConnection,StylistItem,RetailerProfile
from retailers.tasks import *



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
        print permission_url
        return redirect(permission_url)

    return redirect(_return_address(request))

def finalize(request):
    shop_url = request.REQUEST.get('shop')
    try:
        shopify_session = shopify.Session(shop_url, request.REQUEST)
    except shopify.ValidationException:
        messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse('shopify_app.views.login'))

    request.session['shopify'] = {
                "shop_url": shop_url,
                "access_token": shopify_session.token
            }
    messages.info(request, "Logged in to shopify store.")

    response = redirect(_return_address(request))
    request.session.pop('return_to', None)
    return response

def logout(request):
    request.session.pop('shopify', None)
    messages.info(request, "Successfully logged out.")

    return redirect(reverse('shopify_app.views.login'))


@transaction.commit_on_success
@shop_login_required
def load(request,APICONNECTION=ShopifyConnection,ITEM_API_CLASS=ShopifyProduct,VARIATION_API_CLASS= ShopifyVariation):
    shopify_connection,created = APICONNECTION.objects.get_or_create(retailer=request.user,shop_url=request.session['shopify']['shop_url'])
    shopify_connection.access_token = request.session['shopify']['access_token']
    shopify_connection.save()
    update_API_products.delay(shopify_connection)
    return redirect(reverse("product_list"))


