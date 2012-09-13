import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from apps.racks.models import Item as Product
from apps.retailers.models import RetailerProfile
from apps.racks.models import ItemType as ProductInventory
from django.core.paginator import Paginator
from apps.retailers.models import StylistItem

class ProductHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    exclude = (re.compile(r'^private_'), 'category', 'image_urls')
    model = Product

    @classmethod
    def content_size(self, product):
        return len(product.content)

    def read(self, request, pk=None, inventory=None):
        if pk is not None:
            if inventory:
                return ProductInventory.objects.filter(item__pk=pk)
            else:
                return Product.objects.get(pk=int(pk))
        paginator = Paginator(Product.objects.filter(retailers=request.user), 25)
        return paginator.page(int(request.GET.get('page', 1))).object_list

    def update(self, request, pk):
        product = Product.objects.get(id=pk)   
        
        if not request.user in product.retailers.all():
            return rc.FORBIDDEN # returns HTTP 401    

        for (key, value) in request.data.items():
            setattr(product, key, value)
            
        product.save()
        return product
    
    def create(self, request):
        product = Product()
        for (key, value) in request.data.items():
            setattr(product, key, value)
        product.save()
        
        si = StylistItem(stylist=request.user, item=product)
        si.save()
        
        return rc.CREATED        

    def delete(self, request, pk):
        product = Product.objects.get(id=pk)

        if not request.user in product.retailers.all():
            return rc.FORBIDDEN # returns HTTP 401

        product.delete()

        return rc.DELETED # returns HTTP 204
    
class InventoryHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    exclude = (re.compile(r'^private_'), "item",  )
    model = ProductInventory

    def read(self, request, pk):
        return ProductInventory.objects.get(pk=pk)
    
    def update(self, request, pk):
        inventory = ProductInventory.objects.get(id=pk)
        
        if not request.user in inventory.item.retailers.all():
            return rc.FORBIDDEN # returns HTTP 401
        
        for (key, value) in request.data.items():
            setattr(inventory, key, value)
        inventory.save()        

        return inventory
    
    def create(self, request):
        inventory = ProductInventory()
        for (key, value) in request.data.items():
            setattr(inventory, key, value)
        inventory.save()
                
        return rc.CREATED 

    def delete(self, request, pk):
        inventory = ProductInventory.objects.get(id=pk)

        if not request.user in inventory.item.retailers.all():
            return rc.FORBIDDEN # returns HTTP 401

        inventory.delete()

        return rc.DELETED # returns HTTP 204    
    
class RetailerHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')
    exclude = (re.compile(r'^private_'),)
    model = RetailerProfile

    def read(self, request):
        return RetailerProfile.objects.get(user=request.user)

    def update(self, request, id):
        profile = RetailerProfile.objects.get(id=id)
        for (key, value) in request.data.items():
            setattr(profile, key, value)
        profile.save()

        return profile


