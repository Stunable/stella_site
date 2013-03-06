from django.db import models
import os
import sys
from decimal import Decimal
# Create your models here.
from apps.cart.plugins.rate_request import get_rate as fedex_rate_request


CART_ID = 'CART-ID'
from django.conf import settings


class Kart(models.Model):
    creation_date        = models.DateTimeField(auto_now=True)
    checked_out          = models.BooleanField(default=False)
    grand_total          = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)

    def __unicode__(self):
        return unicode(self.creation_date)

    def add_item_variation(self,item_variation):
        
        ki,created      = KartItem.objects.get_or_create(kart=self,item_variation=item_variation,retailer=item_variation.item._retailer)
        ki.unit_price   = item_variation.get_current_price()
        ki.picture      = item_variation.get_image().small.url
        ki.item_name    = item_variation.item.name 

        if not created:
            ki.quantity = ki.quantity + 1
        ki.save()

        self.update_grand_total()

    def add(self,item_variation):
        self.add_item_variation(item_variation)


    def remove(self,item_variation):
        KartItem.objects.get(kart=self,item_variation=item_variation).delete()

    def ref(self):
        return 'asdfasdfasdfasdf'

    def summary(self):
        total = 0
        tax = 0
        processing = 0
        self.items_by_retailer = {}

        retailer = None
        for ki in self.kartitem_set.select_related().all().order_by('retailer'):
            if ki.retailer == retailer:
                self.items_by_retailer[ki.retailer].append(ki)
            else:
                self.items_by_retailer[ki.retailer] = [ki]

            try:
                total += float(ki.total_price)
                tax += float(ki.get_tax_amount())
                print 'total without additional:',total
                processing += ki.get_wepay_amounts()[2]
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
                print('cart processing error:',exc_type, fname, exc_tb.tb_lineno)
        print 'summary:',total,tax,processing
        return total,tax,processing


    def items_by_retailer(self):
        if hasattr(self,'items_by_retailer'):
            return self.items_by_retailer

        self.items_by_retailer = {}

        retailer = None
        for ki in self.kartitem_set.select_related('retailer').all().order_by('retailer'):
            if ki.retailer == retailer:
                self.items_by_retailer[ki.retailer].append(ki)
            else:
                self.items_by_retailer[ki.retailer] = [ki]
        
        return self.items_by_retailer

    def calculate(self):
        total, tax, processing = self.summary()
        self.total = total
        self.tax = tax
        self.processing = processing        
        self.grand_total = Decimal(self.tax + self.total +self.processing + float(self.shipping_and_handling_cost or 0))
        self.checkout_ok = self.check_fee_cost_per_retailer()

    def update_grand_total(self):
        self.grand_total = self.summary()[0]
        self.save()


    @property
    def shipping_and_handling_cost(self):
        return 20



    def check_fee_cost_per_retailer(self):
        for ret,itemlist in self.items_by_retailer.items():
            appfee = 0
            amount = 0
            for item in itemlist:
                appfee += item.get_app_fee()
                amount += item.get_wepay_amounts()[0]
            print appfee/amount
            if appfee/amount > .5:
                return False

        return True

    @staticmethod
    def new(self, request):
        cart = Kart()
        cart.save()
        request.session[CART_ID] = cart.id
        #self.recipient_zipcode = request.session['recipient_zipcode']
        return cart


    def totals_as_dict(self):

        self.calculate()

        return dict(
            total=self.total,
            tax=self.tax,
            shipping_and_handling=float(self.shipping_and_handling_cost),
            processing=float(self.processing),
            grand_total=self.grand_total
        )

    def totals_as_pretty_dict(self):
        d = self.totals_as_dict()
        for k in d.keys():
            d[k] = '%0.2f'%d[k]
        return d


    def update_shipping_for_retailer_item_variations(self,kartitem,shipping_method):
        for ki in self.kartitem_set.filter(retailer=kartitem.retailer):
            ki.shipping_method = kartitem.shipping_method
            ki.save()

    @staticmethod
    def get_by_request(request):
        if request.session.get('cart',None):
            return request.session.get('cart')
        else:
            request.session['cart'] = Kart.objects.create()


    def __iter__(self):
        return iter(self.kartitem_set.select_related('retailer','item_variation','item_variation__size').order_by('retailer'))


    def by_date(self):
        return self.kartitem_set.select_related('retailer','item_variation').order_by('-date_created')


    def count(self):
        return self.kartitem_set.all().count()


def Cart(request):
    return Kart.get_by_request(request)




class KartItem(models.Model):
    kart = models.ForeignKey(Kart)
    
    #normalized info for performance
    item_name       = models.CharField(max_length=255)
    picture         = models.CharField(max_length=255)
    unit_price      = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    quantity        = models.IntegerField(default=1)

    retailer        = models.ForeignKey('retailers.RetailerProfile')
    item_variation  = models.ForeignKey('racks.ItemType')
    shipping_method = models.ForeignKey('retailers.ShippingType', blank=True, null=True)
    date_created    = models.DateTimeField(auto_now=True)


    @property
    def total_price(self):
        return float(self.quantity * self.unit_price)

    @property
    def sub_total(self):
        try:
            return self.total_price + float(self.get_shipping_cost())
        except:
            return self.total_price

    def price_with_shipping(self):
        return float(self.total_price) + float(self.get_shipping_cost())

    @property
    def grand_total(self):
        return float(self.price_with_shipping()) + self.get_tax_amount() + float(self.get_additional_fees())

    @property
    def cost_minus_shipping(self):
        return float(self.total_price) + self.get_tax_amount() + float(self.get_additional_fees())   

    def get_wepay_amounts(self):
        wepay_amount = self.total_price
        # print 'tax amount',self.get_tax_amount()
        wepay_amount += self.get_tax_amount()
        wepay_amount += self.get_shipping_cost()

        wepay_order_amount = wepay_amount + self.get_additional_fees(amount=float(wepay_amount))
        real_wepay_fee = self.get_additional_fees(amount=float(wepay_order_amount))
        amount_customer_pays = wepay_amount + real_wepay_fee

        return (float(wepay_order_amount),float(amount_customer_pays),float(real_wepay_fee))

    def get_app_fee(self):
        return self.total_price * .2 + self.get_shipping_cost()


    def get_retailer(self):
        return self.retailer

    def get_tax_amount(self, buyer=None, zipcode=None, refresh=None):
        return self.total_price * .05
        
    def shipping_amount(self):
        return 1

    def get_shipping_cost(self,refresh=None):
        if not self.shipping_amount or refresh:
            retailer_zipcode = self.retailer.zip_code
            # print 'recipient zip:',self.cart.destination_zip_code
            try:
                self.shipping_amount = fedex_rate_request(shipping_option=self.shipping_method.vendor_tag,weight=self.weight*self.quantity, shipper_zipcode=retailer_zipcode, recipient_zipcode=self.kart.destination_zip_code)
            except:
                self.shipping_amount = 9.95
            self.save()
        return float(self.shipping_amount())

    def get_additional_fees(self, amount=None):
        if not amount:
            amount = self.sub_total
        return settings.WEPAY_FIXED_FEE + settings.WEPAY_PERCENTAGE*.01 * amount