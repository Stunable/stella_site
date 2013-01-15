from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
import shopify
from decorators import shop_login_required

from racks.models import Item,ItemType,Color,Size,ProductImage
from retailers.models import ShopifyProduct,StylistItem


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


@shop_login_required
def load(request):
    products = shopify.Product.find()

    


    for product in products:
        d = product.to_dict()
        # PP.pprint(product.to_dict())

        Map = ShopifyProduct.field_mapping(d)

        PP.pprint(mapping)
        shopify_object,created = ShopifyProduct.objects.get_or_create(source_id=d[Map['API']['source_id']])

        



        if created:
            if len(d['images']):
                url =  d['images'][0]['src']

                out = tempfile.NamedTemporaryFile()
                out.write(urllib.urlopen(url).read())

                Picture = ProductImage.objects.create(image=File(out, os.path.basename(url)),retailer=request.user)



            I = Item.objects.create(
                # brand=brand,
                name =d['title'],
                # description=description,
                image=Picture,
                api_connection = shopify_object
            )

            StylistItem.objects.create(
                                        stylist = request.user,
                                        item = I)


            ItemType.objects.create(
                item = I,
                size = s,
                custom_color_name = color,
                inventory = int(inventory),
                image = Picture,
                price = msrp,
                SKU = SKU
            )



        # if upload.retailer.user:
        #     si = throughModel.objects.create(
        #         stylist = upload.retailer.user,
        #         item = I)
    # for p in products:
    #     PP.pprint(p.to_dict())

    #     print dir(p.variants[0])
    #     v = p.variants[0].to_dict()
    #     v['inventory_quantity'] = 123
    #     p.variants[0] = v

    #     p.save()
       
    # print variations
    orders = shopify.Order.find(limit=3, order="created_at DESC")
    return render_to_response('home/index.html', {
        'products': products,
        'orders': orders,
    }, context_instance=RequestContext(request))
