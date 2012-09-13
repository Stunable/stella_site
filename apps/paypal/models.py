from django.db import models
from django.contrib.auth.models import User
from racks.models import Item
from cart.models import Cart, Purchase
import decimal
import urllib
import sys
from django.conf import settings
from apps.paypal.pro.helpers import PayPalWPP

class Verify(object):
    def __init__(self, tx):
        try:
            Purchase.objects.get(tx=tx)
            self.result = 'Transaction %s has already been processed' % tx
            self.response = self.result
        except Purchase.DoesNotExist:
            post = dict()
            post[ 'cmd' ] = '_notify-synch'
            post[ 'tx' ] = tx
            post[ 'at' ] = settings.PAYPAL_PDT_TOKEN
            self.response = urllib.urlopen(settings.PAYPAL_PDT_URL, urllib.urlencode(post)).read()
            lines = self.response.split('\n')
            self.result = lines[0].strip()
            self.results = dict()
            for line in lines[1:]: # skip first line
                linesplit = line.split('=', 2)
                if len(linesplit) == 2:
                    self.results[ linesplit[0].strip() ] = urllib.unquote(linesplit[1].strip())

    def success(self):
        return self.result == 'SUCCESS' and self.results[ 'payment_status' ] == 'Completed'

    def amount(self):
        return decimal.Decimal(self.results[ 'payment_gross' ])
    
    
"""
    Usage:
        refund_transaction(request, TRANSACTIONID=xxxxxxx)
    Returns:
        {'success': Boolean, 'response': response_detail }
"""
def refund_transaction(request, **kwargs):
    tx = kwargs.get('tx')
    wpp = PayPalWPP(request)
    response = wpp.refundTransaction({'TRANSACTIONID': tx})
    
    ack = response.get('ack')
    
    if ack == "Success" or ack == "SuccessWithWarning": 
        return {'success': True, 'response': response }
    else:
        return {'success': False, 'response': response }

"""
    Usage:
        send_fund(request, email=an@email.com, amt=amount_to_send, email_subject="", note="")
    Returns:
        {'success': Boolean, 'response': response_detail }
"""
def send_fund(request, **kwargs):
    import time
    wpp = PayPalWPP(request)
    response = wpp.massPay({'L_AMT0': kwargs.get('amt'), 
                            'L_EMAIL0': kwargs.get('email'), 
                            'L_UNIQUE0': str(int(time.time())),
                            'L_NOTE0': kwargs.get('note'), 
                            'EMAILSUBJECT': kwargs.get('email_subject')})
    
    ack = response.get('ack')
    if ack == "Success" or ack == "SuccessWithWarning": 
        return {'success': True, 'response': response }
    else:
        return {'success': False, 'response': response } 
        
