from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import shopify
from decorators import shop_login_required

from racks.models import Item,ItemType,Color,Size,ProductImage
from retailers.models import ShopifyProduct,ShopifyVariation,StylistItem
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


    from django.shortcuts import render_to_response
    from django.template import RequestContext
    import shopify
    from decorators import shop_login_required

    import pprint

    PP = pprint.PrettyPrinter(indent=4)


@transaction.commit_on_success
@shop_login_required
def load(request,ITEM_API_CLASS=ShopifyProduct,VARIATION_API_CLASS= ShopifyVariation):
    products = shopify.Product.find()

    for product in products:
        try:
            d = product.to_dict()
            

            PP.pprint(product.to_dict())
            Map = ITEM_API_CLASS.field_mapping(d)

            # PP.pprint(Map)
            api_item_object,created = ITEM_API_CLASS.objects.get_or_create(source_id=d[Map['API']['source_id']])


            # if created:
            if len(d['images']):
                url =  d['images'][0]['src']
                out = tempfile.NamedTemporaryFile()
                out.write(urllib.urlopen(url).read())
                Picture = ProductImage.objects.create(image=File(out, os.path.basename(url)),retailer=request.user)

            I,created = Item.objects.get_or_create(
                # brand=brand,
                name =d['title'],
                # description=description,
                # image=Picture,
                api_type = ContentType.objects.get_for_model(api_item_object),
                object_id = api_item_object.id,
                # api_connection = shopify_object
            )
            I.brand = d[Map['item']['fields']['brand']]
            I.image = Picture
            I.save()

            StylistItem.objects.get_or_create(
                                        stylist = request.user,
                                        item = I)

            for v in d[Map['itemtype']['source']]:

                # PP.pprint(v)

                api_variation_object,created = ShopifyVariation.objects.get_or_create(source_id=v[Map['itemtype']['fields']['source_id']])
                size_string = 'ONE SIZE'
                color_string = 'ONE COLOR'

                # PP.pprint( Map['itemtype']['fields'])
                if Map['itemtype']['fields'].has_key('size'):
                    size_string = v[Map['itemtype']['fields']['size']]

                s,created = Size.objects.get_or_create(
                    size=size_string,
                    retailer = request.user,
                )

                if Map['itemtype']['fields'].has_key('custom_color_name'):
                    color_string =v[Map['itemtype']['fields']['custom_color_name']]
                

                try:
                    it = ItemType.objects.get(
                        item = I,
                        size = s,
                        custom_color_name = color_string
                    )
                except:
                    it = ItemType.objects.create(
                        item = I,
                        size = s,
                        custom_color_name = color_string
                    )


                it.api_type = ContentType.objects.get_for_model(api_variation_object)
                it.object_id = api_variation_object.id
                it.inventory = v[Map['itemtype']['fields']['inventory']]
                it.price = v[Map['itemtype']['fields']['price']]
                it.SKU = v[Map['itemtype']['fields']['SKU']]
                it.image = Picture

                it.save()


                # print it
                # print 'created:',created

                # try:
                #     it.save()
                # except Exception, e:
                #     print 'SAVE ERROR:',str(e)


        except Exception,e:
            raise
            print 'ERROR:',e
       
    # print variations
    # orders = shopify.Order.find(limit=3, order="created_at DESC")
    return redirect(reverse("product_list"))
