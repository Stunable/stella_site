from django.db import models
from django.contrib.auth.models import User

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
            response = WEPAY.call('/checkout/capture', {
                'checkout_id': self.checkout_id
            })

            if response.has_key('state'):
                self.state = response['state']
                self.save()
        
        return self.state


