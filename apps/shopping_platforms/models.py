from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.conf import settings
from tasks import *



class APIProductConnection(models.Model):
    class Meta:
        abstract=True
    source_id = models.IntegerField()
    api_connection= models.ForeignKey('APIConnection')
    parent = models.ForeignKey('self',null=True,blank=True)

    
    def update_inventory(self,item_variation,number_sold):
        raise NotImplementedError('you need to create a method to update the inventory for this api product connection')

class APIPlatformConnection(models.Model):

    class Meta:
        abstract=True
        # these are per API
    ITEM_API_CLASS = "Must be implemented"
    VARIATION_API_CLASS = "Must be implemented"
    
    # these probably won't need to change
    SIZE_CLASS = "Must be implemented"
    ITEM_TYPE_CLASS = "Must be implemented"
    ITEM_CLASS = "Must be implemented"
    IMAGE_CLASS = "Must be implemented"
    # STYLIST_ITEM_CLASS = StylistItem


    variants_Have_Prices = False
    # class Meta:
    #     abstract=True

    #fields
    retailer = models.ForeignKey(User)
    update_in_progress = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)


    @classmethod
    def get_or_create_from_request(cls,request):
        raise NotImplementedError('create an api model instance')


    def refresh_all_products(self):
        if settings.DEBUG:
            update_API_products(self)
        else:
            update_API_products.delay(self)


    def get_variations(self,product_dict):
        return product_dict[self.field_mapping(product_dict)['itemtype']['source']]


    def get_products(self):
        raise NotImplementedError('you need to create a method that returns a list of products for this api')


    def get_url(self):
        return self.api_url

###################################
# these below apply to products and/or variations
###################################
    @staticmethod
    def get_id(pd):
        return pd['id']

    @staticmethod
    def get_images(pd):
        raise NotImplementedError('this needs to output the url/path to the image and some sort of unique identifier to prevent duplicates (path,identifier)')

    @staticmethod
    def get_description(pd):
        raise NotImplementedError('returnds "description')

    @staticmethod
    def get_name(product_dict):
        raise NotImplementedError('returns "name"')

    @staticmethod
    def get_brand(product_dict):
        raise NotImplementedError('should return "brand name"')

    @staticmethod
    def get_prices(variation_object,Map):
        raise NotImplementedError('should return (regular_price,sale_price)')
