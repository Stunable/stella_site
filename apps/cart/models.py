from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from apps.retailers.models import ShippingType
from cart import Cart   
from apps.retailers.models import RetailerProfile
from apps.paypal.pro.helpers import PayPalWPP
from accounts.models import CCToken


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    grand_total = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    shipping_and_handling_cost = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    shipping_method = models.ForeignKey(ShippingType, blank=True, null=True)

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


class Purchase(models.Model):
    cart = models.ForeignKey(Cart)
    purchaser = models.ForeignKey(User)
    purchased_at = models.DateTimeField(auto_now_add=True)
    tx = models.CharField(max_length=250)
    ref = models.CharField(max_length=250, blank=True, null=True)
    shipping_number = models.CharField(max_length=250, blank=True, null=True)
    shipping_method = models.ForeignKey(ShippingType, blank=True, null=True)
    status = models.CharField(max_length=250, default="ordered")
    
    def save(self):
        pk_before_save = self.pk
        
        # generate ref
        self.ref = str(abs(hash(str(self.cart.pk))))[:10] + str(self.purchaser.pk)
        super(Purchase, self).save()
        
        if pk_before_save != self.pk:
            # new order has been made
            
            # notify retailer            
            from apps.notification.models import send_notification_on 
            url = u"http://%s%s" % (
                unicode(Site.objects.get_current()),
                reverse("retailer_order_history"),
            )

            for order_item in self.cart.item_set.all():
                try:
                    send_notification_on("retailer-order-placed", retailer=order_item.product.item.retailers.all()[0],
                                          recipient=order_item.product.item.retailers.all()[0], shopper=self.purchaser, url=url)
                except:
                    # TODO: log error here
                    pass
    
    def name(self):
        return "Shopping with Stella"

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def add(self, product, unit_price, quantity=1, color=None):
        try:
            item = Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except Item.DoesNotExist:
            item = Item(cart=self.cart, product = product, unit_price=unit_price, quantity=quantity, color=color)
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.save()

    
    def summary(self):
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result
    
    def calculate(self):
        self.total = float(self.summary())
        self.tax = self.total * settings.TAX_RATE
        self.shipping_and_handling_cost = 0
        self.grand_total = self.tax + self.total + self.shipping_and_handling_cost

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()
            

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    size = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("size"))
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("color"))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as generic relation
    
    content_type = models.ForeignKey(ContentType)
    
    # foreign key to ItemType
    object_id = models.PositiveIntegerField() 
    objects = ItemManager()
    
    shipping_number = models.CharField(max_length=250, blank=True, null=True)
    shipping_method = models.ForeignKey(ShippingType, blank=True, null=True)
    status = models.CharField(max_length=250, default="ordered")

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)
    
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
        
        purchase = Purchase.objects.filter(cart__item__pk=self.pk)[0]
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

from paypal.pro.signals import payment_was_successful
        
from django.dispatch import receiver    
from models import Cart as CartModel

@receiver(payment_was_successful)
def payment_was_successful_callback(**kwargs):
    params = kwargs['sender']
    if 'nvp_obj' in params and 'request' in params:     
        request = params['request']
        nvp_obj = params['nvp_obj']
        
        cart_id = request.session.get('CART-ID')
        if cart_id:
            try:
                cart = CartModel.objects.get(id=cart_id, checked_out=False)
                
                try:
                    purchase = Purchase.objects.filter(cart=cart)[0]
                except:
                    purchase = Purchase(cart=cart, purchaser=request.user, tx=params['nvp_obj'].transactionid)
                
                if params.get('acct') and nvp_obj.method=="DoDirectPayment":
                    try:
                        # Attempt to save credit token
                        last_four_digits = params.get('acct')[-4:]
                        qs = CCToken.objects.filter(user=request.user, cc_last_four_digits=last_four_digits)
                        
                        if qs.count() == 0:
                            cc_token = CCToken(cc_last_four_digits=last_four_digits, 
                                               user=request.user,
                                               first_name=params.get('firstname', ""),
                                               last_name=params.get('lastname', ""),
                                               token=params['nvp_obj'].transactionid)
                            cc_token.save()
                            
                            if CCToken.objects.filter(user=request.user, is_default=True).count() == 0:
                                cc_token.is_default = True
                                cc_token.save()
                        
                    except:
                        pass
                    
                purchase.save()
            except CartModel.DoesNotExist:
                pass
        
        

