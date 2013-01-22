import os

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField
from racks.models import Item,ProductImage,ItemType,Size
from django.contrib.contenttypes.models import ContentType

import tempfile
import urllib
from django.core.files import File

import shopify
from celery import task

from tasks import process_upload,save_shopify_inventory_update,update_API_products

RETAILER_SUBJECT = 'accounts/retailer_welcome_subject.txt'
RETAILER_MESSAGE = 'accounts/retailer_welcome_message.txt'
    
class ShippingType(models.Model):
    name = models.CharField(max_length=100)
    vendor_tag = models.CharField(max_length=64)
    vendor = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class ProductUpload(models.Model):

    def __unicode__(self):
        try:
            return str(self.retailer)+' | '+str(self.uploaded_zip)
        except:
            return super(ProductUpload,self).__unicode__()

    uploaded_zip = models.FileField(upload_to='product_uploads')
    retailer = models.ForeignKey('RetailerProfile')
    processed = models.BooleanField(default=False)


    def save(self,*args,**kwargs):
        super(ProductUpload, self).save()
        if not self.processed:
            process_upload(self,StylistItem,UploadError)

    def filename(self):
        return os.path.basename(self.uploaded_zip.name)

class UploadError(models.Model):
    def __unicode__(self):
        return self.text
        
    text = models.TextField()
    upload = models.ForeignKey(ProductUpload)

class RetailerProfile(models.Model):
    """
    Company profile model
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    address1 = models.CharField(max_length=255, null=True,blank=True)
    address2 = models.CharField(max_length=255, null=True,blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, choices=US_STATES,null=True,blank=True)
    zip_code = models.CharField(max_length=10,null=True,blank=True)
    hours = models.CharField(max_length=50, null=True, blank=True)
    phone_number = PhoneNumberField(null=True,blank=True)
    email_address = models.EmailField()
    company_logo = models.ImageField(upload_to='upload',null=True,blank=True)
    description = models.TextField()
    selling_options = models.CharField(max_length=100,null=True,blank=True)
    more_details = models.CharField(max_length=100, blank=True, null=True)
    wepay_acct = models.CharField(max_length=64,null=True,blank=True)
    wepay_token = models.CharField(max_length=128,null=True,blank=True)
    shipping_type = models.ManyToManyField(ShippingType, null=True, blank=True)
    accept_refund = models.BooleanField(default=False)
    welcome_message_sent = models.BooleanField(default=False)
    # not_accept_refund = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
#    terms = models.BooleanField(default=False, null=True, blank=True)
    
    def __unicode__(self):
        return self.name.title()
    @property
    def not_accept_refund(self):
        if self.accept_refund:
            return False
        return True
        
    @property
    def logo_image(self):
        """Gets profile picture as a thumbnail and returns the url or returns the default image"""
        return self.company_logo or "upload/default_avatar.gif"
        
    def save(self):
        if self.id:
            old_obj = RetailerProfile.objects.get(pk=self.id)
            if not old_obj.approved and self.approved:
                accept_url = u"http://%s%s" % (
                    unicode(Site.objects.get_current()),
                    reverse("auth_login"),
                )
                ctx = {
                    "accept_url": accept_url,
                    "retailer": self 
                }
                subject = render_to_string(RETAILER_SUBJECT, ctx)
                email_message = render_to_string(RETAILER_MESSAGE, ctx)
                try:
                    new_user = User.objects.get(username=self.email_address)
                    new_user.is_active = True
                    new_user.save()
                    self.user = new_user                    
                except User.DoesNotExist:
                    pass                    
                
#                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [self.email_address])
                send_mail(subject, email_message, settings.STELLA_DEFAULT_EMAIL, [self.email_address])
        super(RetailerProfile, self).save()

    @property
    def firstname(self):
        return self.user.first_name

    @property
    def lastname(self):
        return self.user.last_name

    @property
    def company_name(self):
        return self.name

    @property
    def phone(self):
        return self.phone_number
        
class StylistItem(models.Model):
    stylist = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    
    def __unicode__(self):
        try:
            return self.stylist.username + ' ' + self.item.name
        except:
            return '-deleted- '

class APIProductConnection(models.Model):
    class Meta:
        abstract=True
    source_id = models.IntegerField()
    api_connection= models.ForeignKey('APIConnection')

    



class ShopifyProduct(APIProductConnection):
    pass


class ShopifyVariation(APIProductConnection):

    
    def update_inventory(self,new_value):
        save_shopify_inventory_update.delay(self.api_connection.shopifyconnection,self.source_id,new_value)    


    @staticmethod
    def get_prices(variation_object,Map):
        """ shopify variants don't always have a "compare at price" so we need to handle that"""

        sale_price = variation_object[Map['itemtype']['fields']['sale_price']]
        price = sale_price

        if variation_object[Map['itemtype']['fields']['price']]:
            price = variation_object[Map['itemtype']['fields']['price']]

        return price,sale_price

class APIConnection(models.Model):

    # these are per API
    ITEM_API_CLASS = ShopifyProduct
    VARIATION_API_CLASS = ShopifyVariation
    
    # these probably won't need to change but are helpful for avoiding circular imports
    SIZE_CLASS = Size
    ITEM_TYPE_CLASS = ItemType
    ITEM_CLASS = Item
    IMAGE_CLASS = ProductImage
    STYLIST_ITEM_CLASS = StylistItem

    # class Meta:
    #     abstract=True

    #fields
    retailer = models.ForeignKey(User)
    update_in_progress = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)




class ShopifyConnection(APIConnection):

    def __unicode__(self):
        return self.shop_url

    ITEM_API_CLASS = ShopifyProduct
    VARIATION_API_CLASS = ShopifyVariation

    shop_url = models.TextField()
    access_token = models.TextField()

    def refresh_all_products(self):
        update_API_products.delay(self)

    def get_session(self):
        """ return an object which is authenticated and can interact with the API"""

        session = shopify.Session(self.shop_url)
        session.token = self.access_token
        shopify.ShopifyResource.activate_session(session)
        return shopify

    def get_products(self):
        """ return all products for this retailer for this API"""
        page = 1
        out = []
        while True:
            resp = self.get_session().Product.find(limit=250,page=page)
            if len(resp):
                out += resp
                page += 1
            else:
                return [p.to_dict() for p in out]

    def get_variations(self,product_dict):
        return product_dict[self.field_mapping(product_dict)['itemtype']['source']]

    @staticmethod
    def field_mapping(pd):
        out = {
            'API':{
                'source_id':'id'

            },
            'item':{
                'source':'root',
                'fields':{
                    'name':'title',
                    'category':'product_type',
                    'tags':'tags',
                    'brand':'vendor'
                }
            },
            'itemtype':{
                'source':'variants',
                'fields':{
                    'source_id':'id',
                    'SKU':'sku',
                    'inventory':'inventory_quantity',
                    'price':'compare_at_price',
                    'sale_price':'price',
                    'position':'position'
                }
            }

        }
        for o in pd['options']:
            if o['name'] in ['size','Size']:
                out['itemtype']['fields']['size'] = 'option'+str(o['position'])
            if o['name'] == 'Color':
                out['itemtype']['fields']['custom_color_name'] = 'option'+str(o['position'])

        return out

    @staticmethod
    def get_images(pd):
        for img in pd['images']:
            # this needs to output the url/path to the image and some sort of unique identifier to prevent duplicates
            yield img['src'],img['id']

    @staticmethod
    def get_description(pd):
        desc = ''
        if pd['body_html']:
            desc = pd['body_html']
        return desc



    
    
