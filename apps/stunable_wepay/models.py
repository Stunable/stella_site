from django.db import models
from django.contrib.auth.models import User
from apps.retailers.models import RetailerProfile

import datetime

from django.conf import settings

from wepay import WePay
WEPAY = WePay(settings.WEPAY_PRODUCTION, settings.WEPAY_ACCESS_TOKEN)

class WePayTransaction(models.Model):
    checkout_id = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    retailer = models.ForeignKey(RetailerProfile,null=True)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_modified = models.DateTimeField(auto_now_add=True)

    last_response = models.TextField(null=True,blank=True)

    def capture_funds(self):
        if self.state != 'captured' and self.get_retailer():
            try:
                WEPAY = WePay(settings.WEPAY_PRODUCTION, self.get_retailer().wepay_token)
                response = WEPAY.call('/checkout/capture', {
                    'checkout_id': self.checkout_id
                })

                self.last_response = str(response)
                if response.has_key('state'):
                    self.state = response['state']
                    self.save()
            except:
                raise
        
        return self.state


    def cancel_transaction(self):
        if self.state == 'authorized' and self.get_retailer():
            try:
                WEPAY = WePay(settings.WEPAY_PRODUCTION, self.get_retailer().wepay_token)
                response = WEPAY.call('/checkout/cancel', {
                    'checkout_id'       : self.checkout_id,
                     "cancel_reason"    : "Unintended Purchase (internal testing)"
                })

                self.last_response = str(response)

                if response.has_key('state'):
                    self.state = response['state']
                    self.save()

                    print response
            except:
                raise


    def refund_transaction(self):
        # not implemented
        return


        if self.state == 'authorized' and self.get_retailer():
            try:
                WEPAY = WePay(settings.WEPAY_PRODUCTION, self.get_retailer().wepay_token)
                response = WEPAY.call('/checkout/cancel', {
                    'checkout_id'       : self.checkout_id,
                     "cancel_reason"    : "Unintended Purchase (internal testing)"
                })

                self.last_response = str(response)

                if response.has_key('state'):
                    self.state = response['state']
                    self.save()

                    print response
            except:
                raise


    def get_retailer(self):
        if self.retailer:
            return self.retailer
        try:
            P = self.purchase_set.all()[0]
            R = RetailerProfile.objects.get(user=P.checkout.retailer)
            self.retailer = R
            self.save()
            return R
        except:
            return None


    def get_status(self):
        if self.get_retailer():
            WEPAY = WePay(settings.WEPAY_PRODUCTION, self.get_retailer().wepay_token)

            response = WEPAY.call('/checkout/', {
                'checkout_id': self.checkout_id
            })

            self.last_response = str(response)

            self.state = response['state']
            self.save()




