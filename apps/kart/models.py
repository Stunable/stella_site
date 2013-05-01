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

    user                 = models.ForeignKey('auth.User',null=True,blank=True)
    

    def __unicode__(self):
        return unicode(self.creation_date)

    def available_shipping_options(self):
        return get_shipping_options()

    def manage_variations(self,item_variation,wishlist_only=False,remove=False):
        outval = None
        if not wishlist_only:
            test_ki = KartItem(kart=self,item_variation=item_variation,retailer=item_variation.item._retailer)

            if test_ki.validate_inventory():
                ki,created         = KartItem.objects.get_or_create(kart=self,item_variation=item_variation,retailer=item_variation.item._retailer)
                ki.unit_price      = item_variation.get_current_price()
                try:
                    ki.picture     = item_variation.get_image().small.url
                except:
                    ki.picture     = item_variation.item.get_image().medium.url

                ki.item_name       = item_variation.get_name()

                if created:
                    ki.shipping_method = get_default_shipping()
                    self.total_items = self.total_items + 1
                else:    
                    ki.quantity = ki.quantity + 1
                    
                ki.save()

                self.calculate()
                self.save()

                outval = ki
                message = "This item has been added to your cart.  We will hold it for you for 30 minutes."
            else:
                message = test_ki.get_insufficient_inventory_message()+ "We have added it to your wishlist for safe keeping."

        if self.request.user.is_authenticated():
            user = self.request.user
        else:
            user = None

        existingWIs = WishListItem.objects.filter(item_variation=item_variation,user=user)
        if user and existingWIs.count() and self.request.GET.get('remove',None):
            existingWIs.delete()
            message = 'removed item from wishlist'
        else:
            WI = WishListItem(
                cart=self,
                item_variation=item_variation,
                item=item_variation.item,
                picture = item_variation.get_image(),
                user = user
            )

            WI.save()

            outval = WI
            message = 'added item to wishlist'
            
        return outval,message

    def add(self,item_variation,wishlist_only=False,remove=False):
        return self.manage_variations(item_variation,wishlist_only=wishlist_only,remove=remove)



    def update_info(self,request):
        kartitem = None
        try:
            allowed_attrs = {'shipping_method_id':ShippingType,'quantity':self}
            if request.POST.get('attr') in allowed_attrs.keys():
                att = request.POST.get('attr')

                kartitem = self.items().get(id=request.POST.get('id'))

                if att == 'quantity':
                    if not kartitem.validate_inventory(quantity=int(request.POST.get('val'))):
                        return None,kartitem.get_insufficient_inventory_message()


                setattr(kartitem,att,int(request.POST.get('val')))
                kartitem.save()
                self.calculate()
                self.save() 
                
                return kartitem,None
            else:
                return None,"Sorry, something went wrong please try that again."

        except Exception, e:
            return None,str(e)
            # return e

       


    def remove(self,item_variation):
        self.variationhold_set.filter(variation=item_variation).delete()
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
        #print 'getting cart'
        K = None
        try:
            if checked_out:
                K = Kart.objects.get(id=request.session.get('checked_out_cart'))
                K.request = request
                return K
            if request.user.is_authenticated():
                # if we have a logged in user
                #print 'got user'
                try:
                    # now look for an existing cart that user may have had from a previous session
                    K = Kart.objects.filter(user=request.user,checked_out=False).order_by('-creation_date')[0]
                    #print 'have user kart:',K.id
                except Exception,e:
                    #print 'no user kart:',e
                    K = None

                try:
                    # check for existing carts from the session before the user logged in
                    #print 'getting session cart- id:',request.session.get('cart')
                    sk = Kart.objects.get(id=request.session.get('cart'),user=None)

                    #print 'have session kart'
                except Exception,e:
                    #print 'no old session kart needs converting',e
                    sk = None
            
                if sk and K:
                    #print 'updating existing user kart with incoming session kart'
                    # if we have both a user kart and a session kart, add the session stuff into the user's stuff
                    session_kart_items = sk.kartitem_set.all()

                    session_kart_items.update(kart=K)
                    # change the kart in the sessions items to be the user's kart

                    session_wishlist_items = sk.wishlistitem_set.all()
                    
                    session_wishlist_items.update(user=request.user,cart=K)
                    # do the same with the wish list items 
                    sk.delete()# the old session kart from this user's non logged in state is now empty and unnecessary

            if K:
                request.session['cart'] = K.id
            else:
                # if we haven't found a kart yet, make one
                if not request.session.get('cart',None):
                    K = Kart.objects.create()
                    request.session['cart'] = K.id
                else:
                    K = Kart.objects.get(id=request.session['cart'])
            
            K.request = request

            if not K.user:
                if request.user.is_authenticated():
                    K.user = request.user
                    K.save()
            print 'current kart:',K.id
            return K
        except Exception,e:
            print 'MAJOR CART EXCEPTION', e
            try:
                del(request.session['cart'])
                K = Kart.objects.create()
                request.session['cart'] = K.id
                return K
            except:
                pass

    def __iter__(self):
        return iter(self.items())


    def by_date(self):
        return self.items().order_by('-date_created')


    def get_count(self):
        return self.kartitem_set.all().count()

    def items(self):
        return self.kartitem_set.select_related('retailer','item_variation','item_variation__size','shipping_method').order_by('retailer')

    def release_holds(self):
        self.variationhold_set.all().delete()


    def checkout(self,request):
        # <QueryDict: {u'shipping-address': [u'2'], u'credit-card': [u'1552718934']}>
        shipping_address = ShippingInfo.objects.get(id=request.POST.get('shipping-address'))
        credit_card = CCToken.objects.get(token=request.POST.get('credit-card'))

        wpp = WePayPayment(request,self,credit_card,shipping_address)
        

        success,item_list,error = wpp.authorizePayment()

        print success,item_list,error

        if success:
            self.checked_out = True
            self.save()

            self.release_holds()


            self.wishlistitem_set.all().update(purchased=True)
            request.session['checked_out_cart'] = self.id
            del(request.session['cart'])
            return True,None
        else:
            return False,item_list



def Cart(request,checked_out = False):
    return Kart.get_by_request(request,checked_out)




class KartItem(models.Model):

    def __unicode__(self):
        return self.item_name



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

    def get_tax_rate(self):
        return .05


    def get_tax_amount(self, buyer=None, zipcode=None, refresh=None):
        return self.total_price * self.get_tax_rate()
        
    def shipping_amount(self):
        return float(self.shipping_method.estimated_price)

    def get_shipping_form(self):
        f = modelform_factory(KartItem, fields=("shipping_method",))(instance=self,prefix=self.id)
        f.fields['shipping_method'] = ChoiceField(widget=RadioSelect, choices=((x.id, x) for x in get_shipping_options()))
        f.fields['shipping_method'].widget.attrs = {'data-attr':'shipping_method_id','class':'choiceclick','data-href':'update_info','data-id':self.id}
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


    def get_quantity_select(self,POST=None):
        out = '<span class="hover_toggle change_quantity"><span>change quantity</span>'
        for i in range(1,11):
            out += '<a href="" data-id="%d" data-target="#cart-item-%d" data-val="%d" data-href="update_info/" data-attr="quantity" class="choiceclick">%d</a>'%(self.id,self.id,i,i)
        out += '</span>'
        return out


    def validate_inventory(self,quantity=1):
        total_holds = self.item_variation.get_other_cart_holds(self.kart)
        inventory = self.item_variation.inventory


        print 'holds:',total_holds
        print 'inventory:',inventory
        total_needed = total_holds + quantity

        if inventory >= total_needed:
            return True

        return False

    def get_insufficient_inventory_message(self):
        return "Sorry, but we don't have enough of %s in Size: %s and Color: %s to fulfill your request."%(self.item_variation.item.name, self.item_variation.size,self.item_variation.custom_color_name)

        

    def save(self, *args, **kwargs):
        calculate_cart = False
        if self.id:
            former_self = KartItem.objects.get(id=self.id)
            if self.shipping_method != former_self.shipping_method:
                KIs = KartItem.objects.filter(retailer=self.retailer,kart=self.kart)
                KIs.update(shipping_method=self.shipping_method)
                calculate_cart = True

            if self.quantity != former_self.quantity:
                self.item_variation.update_holds(self.kart,quantity=self.quantity)
                calculate_cart = True

            else:
                super(KartItem,self).save(*args,**kwargs)
                if calculate_cart:
                    self.kart.calculate()
                    self.kart.save()
                return
        super(KartItem,self).save(*args,**kwargs)

        self.item_variation.update_holds(self.kart,quantity=self.quantity)

        



class WishListItem(models.Model):

    item = models.ForeignKey('racks.Item')
    item_variation = models.ForeignKey('racks.ItemType')

    picture = models.ForeignKey('racks.ProductImage')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User',null=True,blank=True)
    cart = models.ForeignKey('kart.Kart',null=True,blank=True)

    purchased = models.BooleanField(default=False)


    def retailer(self):
        return self.item_variation.item._retailer

    def item_name(self):
        return self.item_variation.get_name()






