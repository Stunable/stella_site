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

from tasks import process_upload

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


class APIConnection(models.Model):

    class Meta:
        abstract=True
    retailer = models.ForeignKey(User)
    update_in_progress = models.BooleanField(default=False)


class APIProductConnection(models.Model):
    class Meta:
        abstract=True
    source_id = models.IntegerField()


class ShopifyProduct(APIProductConnection):
    pass

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
                    'price':'price',
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


class ShopifyVariation(APIProductConnection):
    pass




class ShopifyConnection(APIConnection):

    ITEM_API_CLASS = ShopifyProduct
    VARIATION_API_CLASS = ShopifyVariation

    shop_url = models.TextField()
    access_token = models.TextField()

    def get_session(self):
        session = shopify.Session(self.shop_url)
        session.token = self.access_token
        shopify.ShopifyResource.activate_session(session)

        return shopify


    def get_products(self):
        return self.get_session().Product.find()

    def update_products(self):
        for product in self.get_products():
            try:
                d = product.to_dict()
                Map = self.ITEM_API_CLASS.field_mapping(d)

                # PP.pprint(Map)
                api_item_object,created = self.ITEM_API_CLASS.objects.get_or_create(source_id=d[Map['API']['source_id']])

                # if created:
                I,created = Item.objects.get_or_create(
                    name =d['title'],
                    api_type = ContentType.objects.get_for_model(api_item_object),
                    object_id = api_item_object.id,
                )
                I.brand = d[Map['item']['fields']['brand']]
                I.save()
                StylistItem.objects.get_or_create(
                                            stylist = self.retailer,
                                            item = I)

                for index,image in enumerate(self.ITEM_API_CLASS.get_images(d)):
                    path,identifier = image
                    Picture = ProductImage.already_exists(identifier,self.retailer)
                    if not Picture:
                        out = tempfile.NamedTemporaryFile()
                        out.write(urllib.urlopen(path).read())
                        Picture = ProductImage.objects.create(identifier=identifier,image=File(out, os.path.basename(path)),retailer=self.retailer,item=I)

                    if index == 0:
                        I.featured_image = Picture
                        I.save()

                for v in d[Map['itemtype']['source']]:

                    api_variation_object,created = self.VARIATION_API_CLASS.objects.get_or_create(source_id=v[Map['itemtype']['fields']['source_id']])
                    size_string = 'ONE SIZE'
                    color_string = 'ONE COLOR'

                    # PP.pprint( Map['itemtype']['fields'])
                    if Map['itemtype']['fields'].has_key('size'):
                        size_string = v[Map['itemtype']['fields']['size']]

                    s,created = Size.objects.get_or_create(
                        size=size_string,
                        retailer = self.retailer,
                    )

                    if Map['itemtype']['fields'].has_key('custom_color_name'):
                        color_string =v[Map['itemtype']['fields']['custom_color_name']]
                    

                    try:
                        it = ItemType.objects.get(
                            item = I,
                            size = s,
                            custom_color_name = color_string
                        )
                    except:
                        it = ItemType.objects.create(
                            item = I,
                            size = s,
                            custom_color_name = color_string
                        )


                    it.api_type = ContentType.objects.get_for_model(api_variation_object)
                    it.object_id = api_variation_object.id
                    it.inventory = v[Map['itemtype']['fields']['inventory']]
                    it.price = v[Map['itemtype']['fields']['price']]
                    # it.sale_price = v[Map['itemtype']['fields']['sale_price']]
                    it.SKU = v[Map['itemtype']['fields']['SKU']]
                    # it.image = Picture

                    it.save()
            except Exception,e:
                raise
                print 'ERROR:',e
    
