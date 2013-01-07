import datetime
import models
from django.conf import settings


CART_ID = 'CART-ID'


from apps.retailers.models import RetailerProfile,ShippingType


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
            self.set_shipping_option(request.session.get('shipping_method'))

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
            item.quantity = int(quantity)
            item.clor = color
            if size:
                item.size = size
            item.retailer = RetailerProfile.objects.get(item.product.item.retailers.all()[0])
            item.buyer = self.request.user.get_profile()
            item.destination_zip_code = self.recipient_zipcode
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            if item.quantity != quantity:
                item.quantity = int(quantity)
                item.get_tax_amount(buyer=self.request.user.get_profile(),zipcode=self.recipient_zipcode,refresh=True)
                item.get_shipping_cost(recipient_zipcode=self.recipient_zipcode,refresh=True)
            item.color = color


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
        
        self.shipping_and_handling_cost = 0
        
        for item in self.cart.item_set.all():
            try:
                retailer = item.product.item.retailers.all()[0]
                retailer_profile = RetailerProfile.objects.get(user=retailer)
                retailer_zipcode = retailer_profile.zip_code
            except:
                pass

            self.shipping_and_handling_cost += item.get_shipping_cost(recipient_zipcode=self.recipient_zipcode)
            
        self.cart.shipping_and_handling_cost = self.shipping_and_handling_cost
        
        self.cart.save()
            
    def count(self):
        result = 0
        for item in self.cart.item_set.all():
            result += 1 * item.quantity
        return result
        
    def summary(self):
        total = 0
        tax = 0
        processing = 0
        for item in self.cart.item_set.all():
            try:
                total += float(item.total_price)
                tax += float(item.get_tax_amount(buyer=self.request.user.get_profile(),zipcode=self.recipient_zipcode))
                # print 'total without additional:',total
                processing += item.get_wepay_amounts()[2]
            except Exception, e:
                print 'cart processing error:',e
        print 'summary:',total,tax,processing
        return total,tax,processing
    
    def calculate(self):
        total, tax, processing = self.summary()
        self.total = total
        self.tax = tax
        self.processing = processing        
        self.grand_total = self.tax + self.total +self.processing + float(self.cart and self.cart.shipping_and_handling_cost or 0)

    
    def totals_as_dict(self):
        self.calculate()
        return dict(
            total=self.total,
            tax=self.tax,
            shipping_and_handling=float(self.cart.shipping_and_handling_cost),
            processing=float(self.processing),
            grand_total=self.grand_total
        )

    def totals_as_pretty_dict(self):
        d = self.totals_as_dict()
        for k in d.keys():
            d[k] = '%0.2f'%d[k]
        return d


    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

            
    def checkout(self):     
        self.cart.checked_out = True
        self.cart.ref = str(abs(hash(str(self.cart.pk))))[:10] + str(self.request.user.pk)
        self.cart.save()

    def get_shipping_options(self):
        return ShippingType.objects.all()

    def get_shipping_method(self):
        return self.cart.shipping_method

    def set_shipping_option(self,name):
        try:
            option = self.get_shipping_options().filter(name=name)[0]
            self.cart.shipping_method = option
            self.cart.save()
        except Exception,e:
            print 'error setting shipping',e

        self.shipping_method = self.cart.shipping_method

    def get_items_by_retailer(self):
        out = {}
        for item in self.cart.item_set.all():
            r = item.get_product().item.retailers.all()[0]
            if out.has_key(r):
                out[r].append(item)
            else:
                out[r] = [item]

        return out
            #retailer = item.product.item.retailers.all()[0]
            #retailer_profile = RetailerProfile.objects.get(user=retailer)
            #retailer_zipcode = retailer_profile.zip_code





