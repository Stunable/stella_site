# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from paypal.models import Verify
from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart, Purchase
from django.template.context import RequestContext
from apps.paypal.pro.helpers import PayPalWPP

def purchased(request, uid, id):
    # TODO: Not secured
    cart = get_object_or_404(Cart, pk=id)
    user = get_object_or_404(User, pk=uid)
    
    if request.REQUEST.has_key('tx'):
        tx = request.REQUEST['tx']
    try:
        existing = Purchase.objects.get(tx=tx)
        return render_to_response('cart/error.html', 
                                  { 'error': "Duplicate transaction" }, 
                                  context_instance=RequestContext(request) )
    except Purchase.DoesNotExist:
        result = Verify( tx )
        if result.success(): # and resource.amount == result.amount(): # valid
            cart.checked_out = True
            cart.save()
            purchase = Purchase(cart=cart, purchaser=user, tx=tx)
            purchase.save()            
            
            return render_to_response('cart/purchased.html', 
                                      {'cart': cart, 'purchase': purchase }, 
                                      context_instance=RequestContext(request) )
        else: # didn't validate
            return render_to_response('cart/error.html', 
                                      {'error': "Failed to validate payment" }, 
                                      context_instance=RequestContext(request) )
    else: # no tx
        return render_to_response('cart/error.html', 
                                  {'error': "No transaction specified" },
                                  context_instance=RequestContext(request) )
        
        

  
  
  
    
    