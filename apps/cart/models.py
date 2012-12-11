from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.db.models.signals import post_save,pre_save


from apps.retailers.models import ShippingType
from cart import Cart   
from apps.retailers.models import RetailerProfile

from accounts.models import ShippingInfo
from stunable_wepay.models import WePayTransaction

from accounts.models import CCToken

from apps.notification.models import send_notification_on 

from apps.cart.plugins.rate_request import get_rate as fedex_rate_request



from apps.cart.plugins.taxcloud import TaxCloudClient
TCC = TaxCloudClient()



def base35encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789ABCDEFGHIJKLMNOPQRTUVWXYZ'

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]



class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    grand_total = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    shipping_and_handling_cost = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    shipping_method = models.ForeignKey(ShippingType, blank=True, null=True, default=4)

    ref = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

    

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Checkout(models.Model):
    cart = models.ForeignKey('Cart')
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    complete = models.BooleanField(default=False)
    ref = models.CharField(max_length=250, blank=True, null=True)
    retailer = models.ForeignKey(User,blank=True,null=True)

    def check_complete(self):
        try:
            for p in self.purchase_set.all():
                if p.transaction.status != 'captured':
                    return False
        except:
            return False

        self.complete = True
        self.save()

    def save(self,*args,**kwargs):

        super(Checkout, self).save()
        if not self.ref:
            self.ref =base35encode(self.retailer.id+10000)+'S'+base35encode(self.id+10000)
            super(Checkout, self).save()   


class Purchase(models.Model):
    item = models.ForeignKey('Item')
    cart = models.ForeignKey('Cart')
    checkout = models.ForeignKey(Checkout)
    purchaser = models.ForeignKey(User)
    transaction = models.ForeignKey(WePayTransaction)
    ref = models.CharField(max_length=250, blank=True, null=True)
    shipping_number = models.CharField(max_length=250, blank=True, null=True)
    delivery_date = models.DateTimeField(blank=True,null=True)
    shipping_method = models.ForeignKey(ShippingType, blank=True, null=True)
    purchased_at = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        pk_before_save = self.pk
        super(Purchase, self).save()
        
        if pk_before_save != self.pk:
            # new order has been made
            self.ref = str(abs(hash(str(self.pk))))[:10] + str(self.purchaser.pk)
            self.save()
            # notify retailer
            self.notify_retailer()

        if self.shipping_number:
            #if self.transaction.capture_funds() == 'captured':
            self.checkout.check_complete()
            
    def notify_retailer(self):
        url = u"http://%s%s" % (
            unicode(Site.objects.get_current()),
            reverse("retailer_order_history"),
        )

        send_notification_on("retailer-order-placed", retailer=self.checkout.retailer,
                                      recipient=self.checkout.retailer, shopper=self.purchaser, url=url)
        print 'notified retailer'
    
    def name(self):
        return "Shopping with Stella"

    def __iter__(self):
        for item in [self.item]:
            yield item

    def add(self, product, unit_price, quantity=1, color=None):
        try:
            item = self.item
        except Item.DoesNotExist:
            item = Item(cart=self.cart, product = product, unit_price=unit_price, quantity=quantity, color=color)
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.save()

    
    def summary(self):
        return self.item.total_price

    
    def calculate(self):
        self.total = float(self.summary())
        self.tax = self.total * settings.TAX_RATE
        self.shipping_and_handling_cost = 0
        self.grand_total = self.tax + self.total + self.shipping_and_handling_cost

    def clear(self):
        self.item.delete()


    def release_funds(self):
        pass

            
class ShippingLabel(models.Model):
    image = models.ImageField(upload_to="shipping_labels",null=True,blank=True)
    tracking_number = models.CharField(max_length=250, blank=True, null=True)

class Item(models.Model):
    weight = 1

    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    size = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("size"))
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("color"))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    sales_tax_amount = models.DecimalField(default=0, max_digits=18, decimal_places=2, verbose_name=_('sales tax'),null=True,blank=True)
    shipping_amount = models.DecimalField(default=0, max_digits=18, decimal_places=2, verbose_name=_('shipping estimate'),null=True,blank=True)

    destination_zip_code = models.CharField(max_length=10,null=True,blank=True)
    # product as generic relation
    
    content_type = models.ForeignKey(ContentType)
    
    # foreign key to ItemType
    object_id = models.PositiveIntegerField()
    #product = generic.GenericForeignKey('content_type', 'object_id')


    objects = ItemManager()
    
    shipping_number = models.CharField(max_length=250, blank=True, null=True)
    shipping_method = models.ForeignKey(ShippingType, blank=True, null=True)
    shipping_label = models.ForeignKey(ShippingLabel,null=True,blank=True)
    status = models.CharField(max_length=250, default="ordered")

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        try:
            return u'%d - %s' % (self.quantity, self.product)
        except:
            return 'error item'

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    @property
    def sub_total(self):
        try:
            return float(self.total_price) + float(self.shipping_amount)
        except:
            return float(self.total_price)

    def price_with_shipping(self):
        return float(self.total_price) + float(self.shipping_amount)

    @property
    def grand_total(self):
        return float(self.price_with_shipping()) + self.get_tax_amount() + float(self.get_additional_fees())

    @property
    def cost_minus_shipping(self):
        return float(self.total_price) + self.get_tax_amount() + float(self.get_additional_fees())   

    def is_refundable(self):
        return self.status != "refunded"
    
    def is_shippable(self):
        return self.status != "refunded"
    
    def get_actions(self):
        actions = []
        
        if self.is_refundable():
            actions.append({'value': 'return-item', 'name': "Return item"})
            
        if self.is_shippable():
            actions.append({'value': 'ship', 'name': "Ship"})
            
        return actions
            
    @property
    def actions(self): 
        return self.get_actions()

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)
    
    def send_fund_to_retailer(self, request):
        # send money to this retailer
        inventory = self.get_product()
        product = inventory.item
        retailer = product.retailers.all()[0]
        retailer_profile = RetailerProfile.objects.get(user=retailer)
        
        wpp = PayPalWPP(request)
        params = { 'L_AMT0': self.unit_price * self.quantity,  
                   'L_EMAIL0': retailer_profile.paypal_email,
                   'L_UNIQUE0': self.pk,
                   'L_NOTE0': "Fund for purchased item: %s, purchase ref: %s" % (self.pk, self.cart.purchase_set.all()[0].ref),
                   'EMAILSUBJECT': "Fund for purchased item: %s, purchase ref: %s" % (self.pk, self.cart.purchase_set.all()[0].ref) 
                  }
        return wpp.massPay(params)
        
    
    def mark_as_shipped(self, request, tracking_number=None):
        if True or self.status != "shipped":
            self.send_fund_to_retailer(request)
            
            self.status = "shipped"
            self.shipping_number = tracking_number
            self.save()            
                   
            from apps.notification.models import send_notification_on
            from apps.cart.models import Purchase
            shopper = Purchase.objects.filter(cart__item__pk=self.pk)[0].purchaser
            send_notification_on("shopper-item-shipped", shopper=shopper, recipient=shopper, 
                                 order=Purchase.objects.filter(cart__item__pk=self.pk)[0], item=self)
            return True
        
        return False
    
    def refund(self, request):
        wpp = PayPalWPP(request)          
        
        purchase = Purchase.objects.get(item=self)
        response = wpp.refundTransaction({'TRANSACTIONID': purchase.tx, 'REFUNDTYPE': "Partial",  "amt": self.unit_price * self.quantity})
        
        print response
        return response
        
    def return_item(self, request):
        response = None
        if self.status == "ordered" or self.status == "refund_requested":            
            self.status = "refunded"
            self.save()
        
            # refund to shopper
            response = self.refund(request)
            
        
        from apps.notification.models import send_notification_on
        from apps.cart.models import Purchase
        shopper = Purchase.objects.filter(cart__item__pk=self.pk)[0].purchaser
        url = u"http://%s%s" % (
            unicode(Site.objects.get_current()),
            reverse("order_history"),
        )
        send_notification_on("retailer-item-returned", 
                             retailer=self.product.item.retailers.all()[0], 
                             shopper=shopper, 
                             recipient=shopper,
                             order_ref=url)
        
        return response
            
    def cancel_order_return(self):
        self.status = "cancel-order-return"
        self.save()
        
        from apps.notification.models import send_notification_on
        from apps.cart.models import Purchase
        shopper = Purchase.objects.filter(cart__item__pk=self.pk)[0].purchaser
        send_notification_on("retailer-forced-refund", 
                             retailer=self.product.item.retailers.all()[0], 
                             shopper=shopper, 
                             recipient=shopper)

    def get_retailer(self):
        inventory = self.get_product()
        product = inventory.item
        try:
            retailer = product.retailers.all()[0]
        except:
            print 'could not get retailer for item:',product
            return None
        return RetailerProfile.objects.get(user=retailer)

    def get_tax_amount(self, buyer=None, zipcode=None, refresh=None):
        try:
            shipping_address = ShippingInfo.objects.get(customer=buyer,is_default=True)
        except:
            return float(self.total_price) * .05
        retailer = self.get_retailer()
        if retailer:
            if self.sales_tax_amount is None or refresh:
                self.sales_tax_amount = TCC.get_tax_rate_for_item(shipping_address, retailer, [self])
                if self.sales_tax_amount != 0.00:
                    self.save()
                else:
                    return float(self.total_price) * .05
        if self.sales_tax_amount:
            return self.sales_tax_amount
        else:
            return float(self.total_price) * .05

    def get_shipping_cost(self,recipient_zipcode,refresh=None):
        retailer= self.get_retailer()
        if retailer:
            retailer_zipcode = self.get_retailer().zip_code
        else:
            retailer_zipcode = u'10014'

        if not self.shipping_amount or recipient_zipcode != self.destination_zip_code or refresh:
            self.shipping_amount = fedex_rate_request(shipping_option=self.cart.shipping_method.vendor_tag,weight=self.weight*self.quantity, shipper_zipcode=retailer_zipcode, recipient_zipcode=recipient_zipcode)
            self.save()
        return self.shipping_amount

    def get_additional_fees(self):
        return settings.WEPAY_FIXED_FEE + settings.WEPAY_PERCENTAGE*.01 * self.sub_total


from stunable_wepay.signals import payment_was_successful
from django.dispatch import receiver    

@receiver(payment_was_successful,dispatch_uid="payment_authorization_callback")
def payment_was_successful_callback(sender, **kwargs):
    print 'received signal that payment successful for', kwargs['item']
    transaction = sender
    retailer = kwargs['item'].product.item.retailers.all()[0]
    try:
        checkout = Checkout.objects.get(cart=kwargs['item'].cart, retailer=retailer)
    except:
        checkout = Checkout.objects.create(cart=kwargs['item'].cart,retailer=retailer)
    
    p = Purchase.objects.create(
        item = kwargs['item'],
        purchaser = transaction.user,
        transaction = transaction,
        cart = kwargs['item'].cart,
        checkout = checkout,
        shipping_method=kwargs['item'].cart.shipping_method
    )
            
    p.save()

        

