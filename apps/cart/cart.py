import datetime
import models
from django.conf import settings


CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request, instance=None):
        self.request = request
        self.recipient_zipcode = request.session.get('recipient_zipcode')

        if instance:
            self.cart = instance
        else:
            cart_id = request.session.get(CART_ID)
            if cart_id:
                try:
                    cart = models.Cart.objects.get(id=cart_id, checked_out=False)
                except models.Cart.DoesNotExist:
                    cart = self.new(request)
            else:
                cart = self.new(request)
                
            self.cart = cart
            self.cart.shipping_and_handling_cost = cart.shipping_and_handling_cost
            
        self.calculate()
        
    def name(self):
        return "Shopping with Stella"

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        #self.recipient_zipcode = request.session['recipient_zipcode']
        return cart

    def add(self, product, unit_price, quantity=1, size=None, color=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item(cart = self.cart, 
                               product = product,
                               unit_price = unit_price,
                               quantity = quantity,
                               size = size,
                               color = color)
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.size = size
            item.save()

        self.clear_shipping_and_handling_cost()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

        self.clear_shipping_and_handling_cost()

    def update(self, product, unit_price, quantity, size=None, color=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            if unit_price:
                item.unit_price = unit_price
            item.quantity = quantity
            item.clor = color
            if size:
                item.size = size
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = quantity
            item.clor = color
            if size:
                item.size = size
            item.save()
        
        self.clear_shipping_and_handling_cost()
        self.calculate()
        self.cart.grand_total = self.grand_total
        self.cart.save()
    
    def clear_shipping_and_handling_cost(self):    
        # Force re-calculate shipping fee 
        self.cart.shipping_and_handling_cost = 0.0;
        self.cart.save()
        
    def update_shipping_and_handling_cost(self):
        if not self.recipient_zipcode:
            return
        
        from apps.retailers.models import RetailerProfile
        self.shipping_and_handling_cost = 0
        
        for item in self.cart.item_set.all():
            retailer = item.product.item.retailers.all()[0]
            retailer_profile = RetailerProfile.objects.get(user=retailer)
            retailer_zipcode = retailer_profile.zip_code
            from apps.cart.plugins.rate_request import get_rate
            print self.recipient_zipcode
            self.shipping_and_handling_cost += item.quantity * get_rate(weight=1, shipper_zipcode=retailer_zipcode, recipient_zipcode=self.recipient_zipcode)
            
        self.cart.shipping_and_handling_cost = self.shipping_and_handling_cost
        
        self.cart.save()
            
    def count(self):
        result = 0
        for item in self.cart.item_set.all():
            result += 1 * item.quantity
        return result
        
    def summary(self):
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result
    
    def calculate(self):
        self.total = float(self.summary())
        self.tax = self.total * settings.TAX_RATE        
        self.grand_total = self.tax + self.total + float(self.cart and self.cart.shipping_and_handling_cost or 0)
        self.cart.grand_total = self.grand_total
    
    def totals_as_dict(self):
        self.calculate()
        return dict(
            total=self.total,
            tax=self.tax,
            shipping_and_handling=float(self.cart.shipping_and_handling_cost),
            grand_total=self.grand_total
        )

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()


    def set_checkout_id(self,wepay_checkout_id):
        self.cart.checkout_id = wepay_checkout_id
        self.cart.save()
            
    def checkout(self):
        if self.request.GET.get('checkout_id') == self.cart.checkout_id:
            self.cart.checked_out = True
            self.cart.save()
        else:
            raise

