from django.db import models
import os
import sys
from decimal import Decimal
# Create your models here.
from django.db import transaction

from django.forms.models import modelform_factory

from retailers.models import ShippingType
from stunable_wepay.helpers import WePayPayment

from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect

from apps.accounts.models import ShippingInfo,CCToken
import datetime


def get_default_shipping():
    return ShippingType.objects.get(is_default=True)


def get_shipping_options():
    return ShippingType.objects.all()


CART_ID = 'CART-ID'
from django.conf import settings



# self.total = total
#         self.tax = tax
#         self.processing = processing

class Kart(models.Model):
    creation_date        = models.DateTimeField(default=datetime.datetime.now())
    checked_out          = models.BooleanField(default=False)
    
    sub_total            = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    grand_total          = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    total_tax            = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    total_fees           = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    total_shipping       = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)

    total_items          = models.PositiveIntegerField(default=0)
    

    def __unicode__(self):
        return unicode(self.creation_date)

    def available_shipping_options(self):
        return get_shipping_options()

    def manage_variations(self,item_variation,wishlist_only=False):
        if not wishlist_only:
            ki,created         = KartItem.objects.get_or_create(kart=self,item_variation=item_variation,retailer=item_variation.item._retailer)
            ki.unit_price      = item_variation.get_current_price()
            ki.picture         = item_variation.get_image().small.url
            ki.item_name       = item_variation.get_name()

            if created:
                ki.shipping_method = get_default_shipping()
                self.total_items = self.total_items + 1
            else:    
                ki.quantity = ki.quantity + 1
                
            ki.save()

            self.calculate()
            self.save()


        if self.request.user.is_authenticated():
            existingWIs = WishListItem.objects.filter(item_variation=item_variation,user=self.request.user)
            if existingWIs.count():
                existingWIs.delete()

        WI = WishListItem(
            cart=self,
            item_variation=item_variation,
            item=item_variation.item,
            picture = item_variation.get_image(),
        )
        if hasattr(self,'request'):
            if self.request.user.is_authenticated():
                WI.user = self.request.user
        WI.save()
            



    def add(self,item_variation,wishlist_only=False):
        self.manage_variations(item_variation,wishlist_only=wishlist_only)


    def remove(self,item_variation):
        KartItem.objects.get(kart=self,item_variation=item_variation).delete()
        self.calculate()
        self.save()

    def ref(self):
        return 'asdfasdfasdfasdf'

    def summary(self):
        total = 0
        tax = 0
        shipping = 0
        processing = 0
        self.items_by_retailer = {}
        retailer = None

        for ki in self.kartitem_set.select_related().all().order_by('retailer'):
            if self.items_by_retailer.has_key(ki.retailer):
                self.items_by_retailer[ki.retailer].append(ki)
            else:
                self.items_by_retailer[ki.retailer] = [ki]

            try:
                total += float(ki.total_price)
                tax += float(ki.get_tax_amount())
                if retailer != ki.retailer:
                    shipping += ki.get_shipping_cost()
                retailer = ki.retailer
                # print 'total without additional:',total
                processing += ki.get_wepay_amounts()[2]
            except:
                raise
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
                print('cart processing error:',exc_type, fname, exc_tb.tb_lineno)
        return total,tax,processing,shipping


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
        print 'calculating',self
        total, tax, processing,shipping = self.summary()
        self.total_items = self.get_count()
        self.sub_total = total
        self.total_tax = tax
        self.total_fees = processing 
        self.total_shipping = shipping       
        self.grand_total = Decimal(self.total_tax + self.sub_total +self.total_fees + float(self.shipping_and_handling_cost))
        


    @property
    def shipping_and_handling_cost(self):
        return self.total_shipping


    @property
    def checkout_ok(self):
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

    # @staticmethod
    # def new(self, request):
    #     cart = Kart()
    #     cart.save()
    #     request.session[CART_ID] = cart.id
    #     #self.recipient_zipcode = request.session['recipient_zipcode']
    #     return cart


    def totals_as_dict(self):
        # print self.grand_total
        try:
            if int(self.grand_total) == 0:
                # print 'count:',self.get_count()
                # print int(self.grand_total)
                self.calculate()

            return dict(
                total=self.sub_total,
                tax=self.total_tax,
                shipping_and_handling=self.total_shipping,
                processing=self.total_fees,
                grand_total=self.grand_total
            )
        except Exception, e:
            raise
            print 'ERRROR:',e
            pass

    def totals_as_pretty_dict(self):
        try:
            d = self.totals_as_dict()
            for k in d.keys():
                d[k] = '%0.2f'%d[k]
            return d
        except Exception, e:
            print e

    @staticmethod
    def get_by_request(request,checked_out):
        try:
            if checked_out:
                K = Kart.objects.get(id=request.session.get('checked_out_cart'))
                K.request = request
                return K
            if not request.session.get('cart',None):
                K = Kart.objects.create()
                request.session['cart'] = K.id
            else:
                K = Kart.objects.get(id=request.session['cart'])
            K.request = request
            return K
        except:
            del(request.session['cart'])
            K = Kart.objects.create()
            request.session['cart'] = K.id
            return K

    def __iter__(self):
        return iter(self.items())


    def by_date(self):
        return self.items().order_by('-date_created')


    def get_count(self):
        return self.kartitem_set.all().count()

    def items(self):
        return self.kartitem_set.select_related('retailer','item_variation','item_variation__size','shipping_method').order_by('retailer')


    def checkout(self,request):
        # <QueryDict: {u'shipping-address': [u'2'], u'credit-card': [u'1552718934']}>
        shipping_address = ShippingInfo.objects.get(id=request.POST.get('shipping-address'))
        credit_card = CCToken.objects.get(token=request.POST.get('credit-card'))

        wpp = WePayPayment(request,self,credit_card,shipping_address)
        

        success,item_list,error = wpp.authorizePayment()

        print success,item_list,error

        if success:
            self.checked_out = True
            self.wishlistitem_set.all().update(purchased=True)
            request.session['checked_out_cart'] = self.id
            del(request.session['cart'])
            return True,None
        else:
            return False,error



def Cart(request,checked_out = False):
    return Kart.get_by_request(request,checked_out)




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
    def cart(self):
        return self.kart

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
        if self.shipping_method.name == 'Expedited':
            return 20.00
        else:
            return 0

    def get_shipping_form(self):
        f = modelform_factory(KartItem, fields=("shipping_method",))(instance=self,prefix=self.id)
        f.fields['shipping_method'] = ChoiceField(widget=RadioSelect, choices=((x.id, x) for x in get_shipping_options()))
        f.fields['shipping_method'].widget.attrs = {'data-attr':'shipping_method','class':'choiceclick','data-href':'update_info','data-id':self.id}
        return f


    def get_shipping_cost(self,refresh=None):
        # if not self.shipping_amount or refresh:
        #     retailer_zipcode = self.retailer.zip_code
        #     # print 'recipient zip:',self.cart.destination_zip_code
        #     try:
        #         self.shipping_amount = fedex_rate_request(shipping_option=self.shipping_method.vendor_tag,weight=self.weight*self.quantity, shipper_zipcode=retailer_zipcode, recipient_zipcode=self.kart.destination_zip_code)
        #     except:
        #         self.shipping_amount = 9.95
        #     self.save()
        return self.shipping_amount()

    def get_additional_fees(self, amount=None):
        if not amount:
            amount = self.sub_total
        return settings.WEPAY_FIXED_FEE + settings.WEPAY_PERCENTAGE*.01 * amount



    def save(self, *args, **kwargs):
        if self.id:
            if self.shipping_method != KartItem.objects.get(id=self.id).shipping_method:
                KIs = KartItem.objects.filter(retailer=self.retailer,kart=self.kart)
                KIs.update(shipping_method=self.shipping_method)
                self.kart.calculate()
                self.kart.save()

            else:
                super(KartItem,self).save(*args,**kwargs)
                return
        super(KartItem,self).save(*args,**kwargs)



class WishListItem(models.Model):

    item = models.ForeignKey('racks.Item')
    item_variation = models.ForeignKey('racks.ItemType')

    picture = models.ForeignKey('racks.ProductImage')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User',null=True,blank=True)
    cart = models.ForeignKey('kart.Kart',null=True,blank=True)

    purchased = models.BooleanField(default=False)






