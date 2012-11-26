from django.db import models
from django.contrib.auth.models import User
from apps.retailers.models import RetailerProfile

from django.conf import settings

from wepay import WePay
WEPAY = WePay(settings.WEPAY_PRODUCTION, settings.WEPAY_ACCESS_TOKEN)

class WePayTransaction(models.Model):
    checkout_id = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def capture_funds(self):
        if self.state != 'captured':
            try:
                WEPAY = WePay(settings.WEPAY_PRODUCTION, self.get_retailer().wepay_token)

                response = WEPAY.call('/checkout/capture', {
                    'checkout_id': self.checkout_id
                })
                print response
                if response.has_key('state'):
                    self.state = response['state']
                    self.save()
            except:
                raise
        
        return self.state


    def get_retailer(self):
        P = self.purchase_set.all()[0]
        R = RetailerProfile.objects.get(user=P.checkout.retailer)
        return R
