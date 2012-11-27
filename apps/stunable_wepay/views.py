#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.http import urlencode

from django.conf import settings
from stunable_wepay.forms import PaymentForm, ConfirmForm
from accounts.models import UserProfile, CCToken

from wepay import WePay
WEPAY = WePay(settings.WEPAY_PRODUCTION, settings.WEPAY_ACCESS_TOKEN)

class WePayHandleCC(object):
    """
        This was made as a drop in replacement for the PaypalWPP object.
        Functions implemented as needed.

    """
    def __init__(self, item=None, payment_form_cls=PaymentForm,
                 payment_template="cart/payment.html", confirm_form_cls=ConfirmForm, 
                 confirm_template="cart/confirm.html", success_url="/cart/wpp_success/", 
                 fail_url=None, context=None, form_context_name="form"):
        self.item = item
        self.payment_form_cls = payment_form_cls
        self.payment_template = payment_template
        self.confirm_form_cls = confirm_form_cls
        self.confirm_template = confirm_template
        self.success_url = success_url
        self.fail_url = fail_url
        self.context = context or {}
        self.form_context_name = form_context_name

    def __call__(self, request):
        """Return the appropriate response for the state of the transaction."""
        self.request = request
        if request.method == "GET":
            if self.should_render_confirm_form():
                return self.render_confirm_form()
            return self.render_payment_form() 
        else:
            return self.confirm_card_info()
        
        # Default to the rendering the payment form.
        return self.render_payment_form()

    def render_payment_form(self):
        """Display the DirectPayment for entering payment information."""
        self.context[self.form_context_name] = self.payment_form_cls()
        return render_to_response(self.payment_template, self.context, RequestContext(self.request))

    def should_render_confirm_form(self):
        return 'card' in self.request.GET

    def validate_payment_form(self):
        """Try to validate and then process the DirectPayment form."""
        form = self.payment_form_cls(self.request.POST)        
        if form.is_valid():
            success = form.process(self.request, self.item)
            if success:
                return HttpResponseRedirect(self.success_url)
            else:
                self.context['errors'] = self.errors['processing']

        self.context[self.form_context_name] = form
        self.context.setdefault("errors", self.errors['form'])
        return render_to_response(self.payment_template, self.context, RequestContext(self.request))

    def confirm_card_info(self):
        """Post:  {credit_card_id: 1339169043, state: "new"}"""
        try:
            ccID = self.request.POST.get('credit_card_id',None)
            state = self.request.POST.get('state',None)
            if ccID:
                if state == "new":
                    # get some useful display data about this credit card and save in our DB
                    
                    WePay_response = WEPAY.call('/credit_card', {
                              "client_id":settings.WEPAY_CLIENT_ID,
                              "client_secret":settings.WEPAY_CLIENT_SECRET,
                              "credit_card_id":ccID
                            })
                    try:
                        cc_data = WePay_response
                        #  {u'state': u'new', u'create_time': 1350343091, 
                        #  u'credit_card_name': u'Visa xxxxxx4018', 
                        #  u'credit_card_id': 1391197372, 
                        #  u'user_name': u'dave sppon', 
                        #  u'email': u'gdamon@gmail.com'}
                        try:
                            newCC = CCToken.objects.get(cc_name=cc_data['credit_card_name'],user=self.request.user)
                            newCC.token = cc_data['credit_card_id']
                            newCC.user_name = cc_data['user_name']
                            newCC.save()
                        except:
                            newCC,created = CCToken.objects.get_or_create(
                                cc_name = cc_data['credit_card_name'],
                                user_name = cc_data['user_name'],
                                token = cc_data['credit_card_id'],
                                user = self.request.user
                            )
                        #newCC.save()
                        self.current_cc = newCC
                        return self.render_confirm_form()
                    except:
                        raise
        except:
            raise
            print 'ERRORS:',self.request.POST
        
        return self.render_payment_form()


    def render_confirm_form(self):
        """
        Second step of ExpressCheckout. Display an order confirmation form which
        contains hidden fields with the token / PayerID from PayPal.
        """
        #initial = dict(token=self.request.GET['token'], PayerID=self.request.GET['PayerID'])
        print 'rendering confirm form'
        print self.item

        if hasattr(self,'current_cc'):
            cc = self.current_cc
        else:
            if self.request.GET.get('card',None):
                cc = CCToken.objects.get(token=self.request.GET.get('card'))

        self.context['cc'] = cc

        self.context[self.form_context_name] = self.confirm_form_cls(initial=None)
        return render_to_response(self.confirm_template, self.context, RequestContext(self.request))