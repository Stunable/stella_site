from django.shortcuts import render_to_response
from django.template import RequestContext
import shopify
from apps.shopify_app.decorators import shop_login_required

import pprint

PP = pprint.PrettyPrinter(indent=4)

def welcome(request):
    return render_to_response('home/welcome.html', {
        'callback_url': "http://%s/login/finalize" % (request.get_host()),
    }, context_instance=RequestContext(request))

@shop_login_required
def index(request):
    products = shopify.Product.find()

    V = shopify.Variant.find('267157204')

    V.attributes['inventory_quantity'] = 51


    V.save()
    print PP.pprint(V.to_dict())

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

def design(request):
    return render_to_response('home/design.html', {},
                              context_instance=RequestContext(request))


# def load_products(request):
#     products = shopify.Product.find()
#     for p in products:
