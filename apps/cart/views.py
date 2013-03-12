
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
from fedex.base_service import FedexError
from django.template.loader import render_to_string
from retailers.models import ShippingType

from apps.cart.models import Item as CartItem
# from paypal.pro.exceptions import PayPalFailure

from stunable_wepay.views import WePayHandleCC
from stunable_wepay.helpers import WePayPayment
from stunable_wepay.signals import *

from racks.models import Rack

from kart.models import Cart
from django.template.context import RequestContext
from accounts.models import  CCToken
import json
# from paypal.pro.helpers import PayPalWPP
from django.contrib.sites.models import Site

# from apps.cart.plugins.taxcloud import TaxCloudClient
# TCC = TaxCloudClient()

    
import logging
logger = logging.getLogger(__name__)


@login_required
def buy_rack(request, rack_id):

    item_types = []
    R = Rack.objects.get(id=rack_id)
    for I in R.get_rack_items():
        it = ItemType.objects.filter(item=I)
        if len(it):
            item_types.append(it[0])
    for inventory in item_types: 
        product = inventory.item
        cart = Cart(request)    
        cart.add(inventory, product.get_current_price(), 1, inventory.size.size, inventory.color.name)
    return redirect(reverse('get_cart'))

def add_to_cart(request, product_id, wishlist_only=False):
    if request.method == 'POST':
        inventory = ItemType.objects.get(id=product_id)
        cart = Cart(request)    
        cart.add(inventory,wishlist_only=wishlist_only)
    

        return render_to_response("cart/cart_slideout.html", 
                                  {'cart': cart }, 
                                  context_instance=RequestContext(request) )


    return redirect(reverse('get_cart'))


def update_wishlist(request, product_id):
    add_to_cart(request,product_id,wishlist_only=True)

    return HttpResponse(json.dumps({'success':True,'callback':'remove'}, ensure_ascii=False), mimetype='application/json')

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        inventory = ItemType.objects.get(id=product_id)
        cart = Cart(request)
        cart.update(inventory, inventory.item.get_current_price(), quantity, inventory.size.size, inventory.color.name)
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
    

def remove_from_cart(request, product_id):
    product = ItemType.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    if request.is_ajax():
        # totals = cart.totals_as_pretty_dict()
        return HttpResponse(json.dumps({'success':True,'callback':'reload'}),
                            mimetype='application/json') 
    
    return redirect(reverse('get_cart'))


def get_cart(request, template="cart/cart.html"):
    return direct_to_template(request, template, {})

@login_required
def order_history(request, template='orders/user_order_history.html'):
    ctx = {'purchase_actions': 'orders/user_purchase_actions.html'}
    try:
        # shipping_types = ShippingType.objects.all()
        # ctx = {'retailer_profile': retailer_profile, 'shipping_types': shipping_types, 'form': form}
    
        _from = request.GET.get('from')
        _to = request.GET.get('to')

        checkouts = request.user.purchaser_checkout_set.all()
        
        if not _from and not _to:
            checkouts = checkouts.filter(complete=False)
        else:
            if _from:
                checkouts = checkouts.filter(last_modified__gte=_from)
            if _to:
                checkouts = checkouts.filter(last_modified__lte=_to)
                             
        ctx['checkouts']= checkouts.order_by('-last_modified')
    except:
        raise
        #login as regular user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)


def update_info(request, template="cart/info.html"):
    ctx = {}
    allowed_attrs = {'shipping_method':ShippingType}

    cart = Cart(request)
    print request.POST
    if request.method == "POST":
        Ki = cart.items().filter(id=request.POST.get('id'))[0]
        if request.POST.get('attr') in allowed_attrs.keys():
            att = request.POST.get('attr')

            setattr(Ki,att,allowed_attrs[att].objects.get(id=request.POST.get('val')))
            Ki.save()
            return HttpResponse(json.dumps({'success':True,'callback':'reload'}, ensure_ascii=False), mimetype='application/json')

    
    return direct_to_template(request, template, ctx)

@login_required
def update_zipcode(request):
    ret = {'success': False }
    if request.POST:
        request.session['recipient_zipcode'] = request.POST.get('recipient_zipcode')
        request.session['shipping_method'] = request.POST.get('shipping_method')
        cart = Cart(request)        
        try:
            cart.update_shipping_and_handling_cost()
            ret = cart.totals_as_dict()
            ret.update({'success': True})
        except FedexError, e:
            ret['message'] = e.value
            request.session['recipient_zipcode'] = None
    
    return HttpResponse(json.dumps(ret, ensure_ascii=False), mimetype='application/json')
    
    
# from apps.paypal.models import refund_transaction

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


def validate_address(request):

    user_profile = request.user.get_profile()
    try:
        default_ccS = CCToken.objects.filter(user=request.user).order_by('-last_modified')
    except:
        default_ccS = None

    try:
        default_shipping = ShippingInfo.objects.filter(customer=user_profile).filter(is_default=True)[0]
    except:
        default_shipping = None

    ctx =  {  
                'default_ccS': default_ccS,
                'mode':settings.WEPAY_STAGE,
                'wepay_client_id':settings.WEPAY_CLIENT_ID,
                'shipping_form': ShippingInfoForm(request.POST, instance=default_shipping)
            }

    if request.method == "POST":
        shipping_form = ShippingInfoForm(request.POST)
        if shipping_form.is_valid():
            shipping_info = shipping_form.save(commit=False)
            shipping_info.customer=user_profile
            shipping_info.is_default=True
            shipping_info.save()

            shipping_addresses = ShippingInfo.objects.filter(customer=user_profile)
            return HttpResponse(json.dumps(
                {
                    'success':True,
                    'html': render_to_string("includes/shipping_address_choices.html", {'shipping_addresses':shipping_addresses})
                }

            ), mimetype='application/json') 

            
        else:
            return HttpResponse(json.dumps(
                {
                    'success':False,
                    'html': render_to_string("includes/shipping_address_form.html", {'shipping_form':shipping_form})
                }

            ), mimetype='application/json') 
            
           

    return direct_to_template(request,  "cart/payment.html", ctx)

def validate_cc(request,*args,**kw):

    user_profile = request.user.get_profile()
    try:
        default_ccS = CCToken.objects.filter(user=request.user).order_by('-last_modified')
    except:
        default_ccS = None


    ctx =  {  
                'default_ccS': default_ccS,
                'mode':settings.WEPAY_STAGE,
                'wepay_client_id':settings.WEPAY_CLIENT_ID,
            }



    ppp = WePayHandleCC(**kw)
    if ppp.confirm_card_info(request=request,return_valid=True):
        default_ccS = CCToken.objects.filter(user=request.user).order_by('-last_modified')

        return HttpResponse(json.dumps(
                {
                    'success':True,
                    'html': render_to_string("includes/credit_card_choices.html", {'default_ccS':default_ccS})
                }

            ), mimetype='application/json') 
    else:
        return HttpResponse(json.dumps(
                {
                    'success':False,
                    'html': "There was a strange error processing your card.  Maybe try a different one?"
                }

            ), mimetype='application/json') 




           

    return direct_to_template(request,  "cart/payment.html", ctx)


@login_required
def wpp(request):    
    cart = Cart(request)
    user_profile = request.user.get_profile()
    
    
    try:
        default_ccS = CCToken.objects.filter(user=request.user).order_by('-last_modified')
    except:
        default_ccS = None
    try:
        default_shipping = ShippingInfo.objects.filter(customer=user_profile).filter(is_default=True)[0]
    except:
        default_shipping = None


    shipping_addresses = ShippingInfo.objects.filter(customer=user_profile)




    # shipping_form = ShippingInfoForm(request.POST, instance=default_shipping)
    #     if shipping_form.is_valid():
    #         shipping_info = shipping_form.save(commit=False)
    #         shipping_info.customer=user_profile
    #         if not default_shipping:
    #             shipping_info.is_default=True
    #         shipping_info.save()
    #         return HttpResponseRedirect(reverse('express_checkout'))
    #     else:
    #         ctx['shipping'] = shipping_form



    kw = {
      "context": {  'cart':cart, 
                    'default_ccS': default_ccS,
                    'mode':settings.WEPAY_STAGE,
                    'wepay_client_id':settings.WEPAY_CLIENT_ID,
                    'shipping_form': ShippingInfoForm(),
                    'shipping_addresses':shipping_addresses,

                    },
                          # what you're selling
      "payment_template": "cart/payment.html",      # template name for payment
      "confirm_template": "cart/confirm.html", # template name for confirmation
      "success_url": "/cart/wpp_success/"}              # redirect location after success
    
    ppp = WePayHandleCC(**kw)
    return ppp(request)


@login_required
def place_order(request):
    
    if request.method == "POST":
        cart = Cart(request)
    #current_cart.cart.save()
    
        result,error = cart.checkout(request)

        if result is True:
            return HttpResponse(json.dumps(
                {
                    'success':True,
                    'redirect': '/cart/success'
                }

            ), mimetype='application/json') 
        else:
            return HttpResponse(json.dumps(
                {
                    'success':False,
                    'error': str(error)
                }

            ), mimetype='application/json')  



@login_required
def wpp_success(request):
    
    current_cart = Cart(request,checked_out=True)
    #current_cart.cart.save()
    
    try:        
        return render_to_response('cart/purchased.html', 
                                  {'cart': current_cart, 'checkouts':current_cart.checkout_set.all() }, 
                                  context_instance=RequestContext(request) )
    except: 
        raise
        return render_to_response('cart/error.html', 
                                  {'error': "Failed to validate payment" }, 
                                  context_instance=RequestContext(request) )
        
        
@login_required
def wpp_reference_pay(request):
    cc_token = None
    if request.GET.get('card',None):
        try:
            cc_token = CCToken.objects.get(user=request.user, token=request.GET.get('card'))
        except:
            print 'evil is afoot?'
    if not cc_token:
        cc_tokens = CCToken.objects.filter(user=request.user, is_default=True)
        if cc_tokens.count()==0:
            return render_to_response('cart/error.html', 
                                      {'error': "You do not have default credit card, and you didn't specify one. A Default credit card should be available after a first successful transaction" }, 
                                      context_instance=RequestContext(request))
        else:
            cc_token = cc_tokens[0]
    try:
        current_cart = Cart(request)
        if not current_cart.cart.checked_out:
            wpp = WePayPayment(request,current_cart,cc_token)
            wpp.authorizePayment()
    except:
        raise
        return render_to_response('cart/error.html', 
                                  {'error': "Can not proccess payment, please contact us at payment@stunable.com" }, 
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('wpp_success'))
    
    
    