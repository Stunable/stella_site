from cart import Cart
from racks.models import Item as Product
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings
from apps.accounts.forms import BillingInfoForm, ShippingInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from apps.accounts.models import ShippingInfo
from apps.cart.models import Purchase
from django.contrib.auth.decorators import login_required
from apps.racks.models import ItemType
from apps.cart.plugins.fedex.base_service import FedexError

from apps.cart.models import Item as CartItem
from paypal.pro.exceptions import PayPalFailure
from paypal.pro.views import PayPalPro
from apps.cart.cart import Cart
from django.template.context import RequestContext
from accounts.models import UserProfile, CCToken
import json
from paypal.pro.helpers import PayPalWPP
from django.contrib.sites.models import Site

try:
    import simplejson as json
except ImportError:
    import json
    
import logging
logger = logging.getLogger(__name__)

from wepay import WePay

@login_required
def add_to_cart(request, product_id, quantity, size=None):
    inventory = ItemType.objects.get(id=product_id)
    product = inventory.item
    cart = Cart(request)    
    cart.add(inventory, product.price, quantity, inventory.size.size, inventory.color.name)
    
    return redirect(reverse('get_cart'))

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        inventory = ItemType.objects.get(id=product_id)
        cart = Cart(request)
        cart.update(inventory, inventory.item.price, quantity, inventory.size.size, inventory.color.name)
        if request.is_ajax():
            try:
                if request.session.get('recipient_zipcode'):
                    cart.update_shipping_and_handling_cost()
            except:
                pass
                
            totals = cart.totals_as_dict()
            totals.update(dict(quantity=quantity, size=inventory.size.size))
            
            return HttpResponse(json.dumps(totals),
                                mimetype='application/json') 
        
        return redirect(reverse('get_cart'))
    
@login_required
def remove_from_cart(request, product_id):
    product = ItemType.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    if request.is_ajax():
        totals = cart.totals_as_dict()
        return HttpResponse(json.dumps(totals),
                            mimetype='application/json') 
    
    return redirect(reverse('get_cart'))

@login_required
def get_cart(request, template="cart/cart.html"):
    return direct_to_template(request, template, {})

@login_required
def order_history(request, template='cart/order_history.html'):
    try:
        ctx = {
               'purchases': Purchase.objects.filter(purchaser=request.user).order_by('-purchased_at')
        }
    except:
        ctx = {}
    
    return direct_to_template(request, template, ctx)

@login_required
def update_info(request, template="cart/info.html"):
    cart = Cart(request)
    
    if cart.cart and not cart.cart.shipping_and_handling_cost:
        return redirect(reverse('get_cart'))
    
    ctx = {}

    try:
        user_profile = request.user.get_profile()
    except:
        user_profile = None

    try:
        default_shipping = ShippingInfo.objects.filter(customer=user_profile).filter(is_default=True)[0]
    except:
        default_shipping = None

    if request.method=='GET':
        ctx.update(
                {"shipping": ShippingInfoForm(instance=default_shipping, prefix="shipping", 
                                              initial={'customer':user_profile, 
                                                       'zip_code':request.session.get('recipient_zipcode')}), 
        })

    else:
        response = {'success' : True, 'errors': {}}            
        form_data = request.POST.copy()
        shipping_form = ShippingInfoForm(form_data, prefix="shipping", instance=default_shipping)
        
        if not shipping_form.is_valid():
            response.update({'success' : False})
            response['errors'].update(shipping_form.errors)
        
        if not request.POST.get('term_and_condition'):
            response.update({'success' : False})
            response['errors'].update({'term_and_condition': ['Accepting Term and condition is requred.']})
        
        if response['success']:
            shipping_info = shipping_form.save(commit=False)
            shipping_info.customer=user_profile
            if not default_shipping:
                shipping_info.is_default=True
            shipping_info.save()
                                
        return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
    
    return direct_to_template(request, template, ctx)

@login_required
def update_zipcode(request):
    ret = {'success': False }
    if request.POST:
        request.session['recipient_zipcode'] = request.POST.get('recipient_zipcode')
        cart = Cart(request)        
        try:
            cart.update_shipping_and_handling_cost()
            ret = cart.totals_as_dict()
            ret.update({'success': True})
        except FedexError, e:
            ret['message'] = e.value
            request.session['recipient_zipcode'] = None
    
    return HttpResponse(json.dumps(ret, ensure_ascii=False), mimetype='application/json')
    
    
from apps.paypal.models import refund_transaction

@login_required
def shopper_return_purchase(request):
    if request.method != 'POST':
        response = {'success': False, 'message': 'Not allowed'}
    else:
        item_id = request.POST.get('item_id')        
        response = refund_transaction(request, tx=request.POST.get('transactionid'))
    
    return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')


@login_required
def shopper_request_refund_item(request):
    response = {'success': False, 'message': 'Not allowed'}
    if request.method == 'POST':
        transaction_id = request.POST.get('transactionid')
        item_id =request.POST.get('item_id')
        
        try:
            ci = CartItem.objects.get(pk=item_id, cart__purchase__tx=transaction_id)
            
            # verify if user is the retailer who sales this items
            if ci.status != "refund_requested":
                ci.status = "refund_requested"
                ci.save()
                from apps.notification.models import send_notification_on
                shopper = Purchase.objects.filter(cart__item__pk=ci.pk)[0].purchaser
                url = u"http://%s%s" % (
                    unicode(Site.objects.get_current()),
                    reverse("retailer_order_history"),
                )
                send_notification_on("shopper-refund-requested", 
                                     retailer=ci.product.item.retailers.all()[0], 
                                     shopper=shopper, 
                                     recipient=ci.product.item.retailers.all()[0],
                                     order=Purchase.objects.filter(cart__item__pk=ci.pk)[0],
                                     url=url)
                response = {'success': True, 
                            'message': 'Refund request has been sent to retailer successfully',
                            'item': {'id': ci.pk, 'status': ci.status}}
        except Exception, e:
            response.update({'message': str(e)})
    
    return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')

@login_required
def shopper_return_item(request):
    response = {'success': False, 'message': 'Not allowed'}
    if request.method == 'POST':
        # Lookup for the amount of the item id        
        transaction_id = request.POST.get('transactionid')
        item_id =request.POST.get('item_id')
        
        try:
            ci = CartItem.objects.get(pk=item_id, cart__purchase__tx=transaction_id)
            
            # verify if user is the retailer who sales this item
            if ci.status != "refunded":                
                amount = ci.quantity * ci.unit_price
                response = refund_transaction(request, tx=request.POST.get('transactionid'), REFUNDTYPE="partial", amt=amount)
                
                # refund this item
                ci.status = "refunded"
                ci.save()
                
                response.update({'item': {'id': ci.pk, 'status': ci.status}})
            else:
                message = "The item is already refunded"
            
        except CartItem.DoesNotExist:
            message = 'Not allowed'
        except PayPalFailure:
            message = "No permission"
        except Exception, e:
            logging.error(e)
            message = "Interal error"
            
        response['message'] = message
    
    return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')

@login_required
def wpp(request): 


    # set production to True for live environments
    cart = Cart(request)
    
    wepay = WePay(settings.WEPAY_PRODUCTION, settings.WEPAY_ACCESS_TOKEN)
    
    # create the checkout
    response = wepay.call('/checkout/create', {
        'account_id': settings.WEPAY_CLIENT_ID,
        'amount': cart.grand_total,
        'short_description': cart.name(),
        'type': 'GOODS',
        'mode': 'iframe',
        'redirect_uri':settings.WWW_ROOT.rstrip('/')+reverse('wpp_success')
    })
    # display the response
    WePay_response = response

    cart.set_checkout_id(WePay_response['checkout_id'])
    
    item = {"amt": cart.grand_total,             # amount to charge for item
        "inv": cart.name(),         # unique tracking variable paypal
        "custom": "tracking",       # custom tracking variable for you
        "cancelurl": 'http://' + request.META['HTTP_HOST'] + "/cart/wpp",  # Express checkout cancel url
        "returnurl": 'http://' + request.META['HTTP_HOST'] + "/cart/wpp" }  # Express checkout return url
    
    try:
        default_cc = CCToken.objects.filter(user=request.user, is_default=True)[0]
    except:
        default_cc = None
    
    kw = {
      "context": {'default_cc': default_cc},
      "item": item,                            # what you're selling
      "payment_template": "cart/payment.html",      # template name for payment
      "confirm_template": "cart/confirm.html", # template name for confirmation
      "success_url": "/cart/wpp_success/"}              # redirect location after success
    
    # ppp = PayPalPro(**kw)
    # return ppp(request)

    return render_to_response('cart/payment.html', 
                              {'wepay': WePay_response }, 
                              context_instance=RequestContext(request) )


@login_required
def wpp_success(request):
    purchase = None

    current_cart = Cart(request)
    current_cart.cart.save()
    
    # update grand total
    
    # try:        
    current_cart.checkout()
    #purchase = Purchase.objects.filter(cart=current_cart.cart)[0]
    return render_to_response('cart/purchased.html', 
                              {'cart': Cart(request), 'purchase': current_cart }, 
                              context_instance=RequestContext(request) )
    # except: 
    #     return render_to_response('cart/error.html', 
    #                               {'error': "Failed to validate payment" }, 
    #                               context_instance=RequestContext(request) )
        
        
@login_required
def wpp_reference_pay(request):
    cc_tokens = CCToken.objects.filter(user=request.user, is_default=True)
    if cc_tokens.count()==0:
        return render_to_response('cart/error.html', 
                                  {'error': "You do not have default credit cart, default credit card should be availalbe after a first successful transaction" }, 
                                  context_instance=RequestContext(request))
    else:
        cc_token = cc_tokens[0]
    
    try:
        wpp = PayPalWPP(request)
        current_cart = Cart(request)
        wpp.doReferenceTransaction(
                                    {'REFERENCEID': cc_token.token, 
                                    'AMT': current_cart.grand_total,
                                    'IPADDRESS': request.META.get('REMOTE_ADDR', '').split(':')[0],
                                    'DESC': 'ShopWithStella',
                                    'FIRSTNAME': cc_token.first_name,
                                    'LASTNAME': cc_token.last_name})
    except PayPalFailure:
        return render_to_response('cart/error.html', 
                                  {'error': "Can not proccess payment, please pay by alternative method" }, 
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('wpp_success'))
    
    
    