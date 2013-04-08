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
import shopify

import apps.portable as portable

from apps.common.forms import FedexTestAddress

from tasks import process_upload,save_shopify_inventory_update,update_API_products



RETAILER_SUBJECT = 'accounts/retailer_welcome_subject.txt'
RETAILER_MESSAGE = 'accounts/retailer_welcome_message.txt'
NEW_UPLOAD = 'retailers/new_upload.txt'
    
class ShippingType(models.Model):


    name = models.CharField(max_length=100)
    vendor_tag = models.CharField(max_length=64)
    vendor = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    price_description = models.CharField(max_length=200, default="Free Today Only!")
    estimated_price = models.DecimalField(default=0.00,max_digits=10, decimal_places=2)
    estimated_arrival_time = models.CharField(max_length=200,default="3-5 days")
    
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
            ctx = {
                   'upload': self,

                }
            subject = 'stunable.com upload %d'%self.id
            email_message = render_to_string(NEW_UPLOAD, ctx)
                      
            
#                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [self.email_address])
            send_mail(subject, email_message, settings.RETAILER_EMAIL, [self.retailer.email_address])

            email_message = "%sadmin/retailers/productupload/%d/ was uploaded by %s\n\n"%(settings.WWW_ROOT,self.id,self.retailer.email_address) + email_message
            send_mail(subject, email_message, settings.EMAIL_HOST_USER, [settings.RETAILER_EMAIL])
            # process_upload(self,StylistItem,UploadError)

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
    not_accept_refund = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
#    terms = models.BooleanField(default=False, null=True, blank=True)
    
    def __unicode__(self):
        try:
            return self.name.title()
        except:
            return 'Retailer Profile Object'

    # @property
    # def not_accept_refund(self):
    #     if self.accept_refund:
    #         return False
    #     return True
        
    @property
    def logo_image(self):
        """Gets profile picture as a thumbnail and returns the url or returns the default image"""
        return self.company_logo or "upload/default_avatar.gif"
        
    def save(self):
        if self.id:
            old_obj = RetailerProfile.objects.get(pk=self.id)
            if not old_obj.approved and self.approved:
                url = u"%s%s" % (
                    settings.RETAILER_SUBDOMAIN.rstrip('/'),
                    reverse("auth_login"),
                )
                ctx = {
                    "accept_url": url,
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
                send_mail(subject, email_message, settings.EMAIL_HOST_USER, [self.email_address])
                subject = "NEW RETAILER:%s"%self.name
                email_message = "THE FOLLOWING EMAIL WAS SENT TO %s\n"%self.email_address + email_message
                send_mail(subject, email_message, settings.EMAIL_HOST_USER, [settings.RETAILER_EMAIL])
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

    @staticmethod
    def verify_address(data=None):

        F = FedexTestAddress(data)
        return F.validate().processed()


    def admin_link(self):
      return '<a href="%s?retailer=%s">admin page link</a>' %(reverse('product_list'),self.id)

    admin_link.allow_tags = True

    def return_policy(self):
        if self.accept_refund:
            return "14 days"
        else:
            return "No Returns"


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
    parent = models.ForeignKey('self',null=True,blank=True)

    
    def update_inventory(self,item_variation,number_sold):
        raise NotImplementedError('you need to create a method to update the inventory for this api product connection')
            

class ShopifyProduct(APIProductConnection):
    pass


class ShopifyVariation(APIProductConnection):

    def update_inventory(self,item_variation,number_sold):

        save_shopify_inventory_update.delay(self.api_connection.shopifyconnection,self.source_id,item_variation,number_sold)    


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


    variants_Have_Prices = False
    # class Meta:
    #     abstract=True

    #fields
    retailer = models.ForeignKey(User)
    update_in_progress = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)




class APIConnectionMixin(object):

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

class ShopifyConnection(APIConnection,APIConnectionMixin):

    def __unicode__(self):
        return self.shop_url

    ITEM_API_CLASS = ShopifyProduct
    VARIATION_API_CLASS = ShopifyVariation

    shop_url = models.TextField()
    access_token = models.TextField()

    
    variants_Have_Prices = True

    def get_session(self):
        """ return an object which is authenticated and can interact with the API"""

        session = shopify.Session(self.shop_url)
        session.token = self.access_token
        shopify.ShopifyResource.activate_session(session)
        return shopify

    def get_products(self):
        """ return all products for this retailer for this API"""
        page = 1

        while True:
            resp = self.get_session().Product.find(limit=10,page=page)
            if not len(resp):
                return
            yield [p.to_dict() for p in  resp]
            page += 1
       
    

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
            if o['name'] in ['size','Size','Chain Lengh',]:
                out['itemtype']['fields']['size'] = 'option'+str(o['position'])
            if o['name'] in['color', 'Color', 'Style', 'style']:
                out['itemtype']['fields']['custom_color_name'] = 'option'+str(o['position'])

        if not out['itemtype']['fields'].get('custom_color_name',None) and not out['itemtype']['fields'].get('size',None):
            print "COULD NOT FIND COLOR OR SIZE IN:",pd['options']

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


class PortableProduct(APIProductConnection):
    pass

    @staticmethod
    def get_prices(pd):
        return float(pd['price'])/100,float(pd['sale_price'])/100


class PortableVariation(APIProductConnection):
    pass


class PortableConnection(APIConnection,APIConnectionMixin):

    def __unicode__(self):
        return self.api_url+self.access_token

    ITEM_API_CLASS = PortableProduct
    VARIATION_API_CLASS = PortableVariation

    api_url = 'https://api.portableshops.com/'
    access_token = models.CharField(max_length=64,null=True)


    variants_Have_Prices = False


    def get_products(self):
        api = portable.ShoppingPlatformAPI(self)

        l = api.extract_product_list()
        return api.extract_product_list()

    @staticmethod
    def get_full_size_media_path(data):
        out = [data['media_server_id']]
        out.extend(
            [
                data['media_dimension']['template']['width'],
                data['media_dimension']['template']['height'],
                data['media_dimension']['template']['extension']
            ]
        )

        return '.'.join(out)

    @staticmethod
    def get_images(pd):
        path = 'http://images.portableshops.com/'
        yield path+ self.get_full_size_media_path(pd['primary_media']),pd['primary_media']['id']
        for img in pd['media']:
            yield path+ self.get_full_size_media_path(img)
       
    @staticmethod
    def field_mapping(pd):
        out = {
            'API':{
                'source_id':'id'
            },
            'item':{
                'source':'item',
                'fields':{
                    'name':'name',
                    'category':'product_type',
                    'tags':'tags',
                    'brand':'designer_name'
                }
            },
            'itemtype':{
                'source':'variation',
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
            if o['name'] in ['size','Size','Chain Lengh',]:
                out['itemtype']['fields']['size'] = 'option'+str(o['position'])
            if o['name'] in['color', 'Color', 'Style', 'style']:
                out['itemtype']['fields']['custom_color_name'] = 'option'+str(o['position'])

        if not out['itemtype']['fields'].get('custom_color_name',None) and not out['itemtype']['fields'].get('size',None):
            print "COULD NOT FIND COLOR OR SIZE IN:",pd['options']

        return out


"""
    {   u'item': {   u'condition_id': u'2',
                     u'created': u'2013-04-06 11:48:00',
                     u'description': u'<p>nice jeans, couple of holes...</p>',
                     u'designer_name': u'deisel',
                     u'featured': u'0',
                     u'friendly_url': u'my_jeans',
                     u'id': u'16903',
                     u'item_collection_id': u'16185',
                     u'modified': u'2013-04-07 08:01:08',
                     u'name': u'my jeans',
                     u'price': u'10000',
                     u'primary_media': u'75308',
                     u'sale_price': u'7999',
                     u'sort': u'1',
                     u'swappable': u'0',
                     u'visible': u'1'},
        u'media': [   {   u'caption': u'',
                          u'created': u'2013-04-06 11:49:38',
                          u'extension': u'jpg',
                          u'id': u'75308',
                          u'item_id': u'16903',
                          u'jobs_remaining': u'',
                          u'media_dimension': {   u'': {   u'height': u'269',
                                                           u'width': u'190'},
                                                  u'facebook': {   u'height': u'220',
                                                                   u'width': u'150'},
                                                  u'keep_size': {   u'height': u'0',
                                                                    u'width': u'0'},
                                                  u'project_thumb': {   u'height': u'137',
                                                                        u'width': u'137'},
                                                  u'small_thumb': {   u'height': u'50',
                                                                      u'width': u'50'},
                                                  u'store_main': {   u'height': u'585',
                                                                     u'width': u'384'},
                                                  u'store_thumb': {   u'height': u'216',
                                                                      u'width': u'144'},
                                                  u'store_thumb2': {   u'height': u'64',
                                                                       u'width': u'64'},
                                                  u'template': {   u'height': u'422',
                                                                   u'width': u'670'},
                                                  u'thumb': {   u'height': u'150',
                                                                u'width': u'150'}},
                          u'media_server_id': u'515f71224fe59',
                          u'media_type_id': u'0',
                          u'media_variation': [],
                          u'mimetype': u'',
                          u'modified': u'2013-04-07 08:01:08',
                          u's3': u'1',
                          u'size': u'132909',
                          u'sort': u'1',
                          u'user_id': u'35443'},
                      {   u'caption': u'',
                          u'created': u'2013-04-06 11:49:21',
                          u'extension': u'jpg',
                          u'id': u'75307',
                          u'item_id': u'16903',
                          u'jobs_remaining': u'',
                          u'media_dimension': {   u'': {   u'height': u'269',
                                                           u'width': u'190'},
                                                  u'facebook': {   u'height': u'220',
                                                                   u'width': u'150'},
                                                  u'keep_size': {   u'height': u'0',
                                                                    u'width': u'0'},
                                                  u'project_thumb': {   u'height': u'137',
                                                                        u'width': u'137'},
                                                  u'small_thumb': {   u'height': u'50',
                                                                      u'width': u'50'},
                                                  u'store_main': {   u'height': u'585',
                                                                     u'width': u'384'},
                                                  u'store_thumb': {   u'height': u'216',
                                                                      u'width': u'144'},
                                                  u'store_thumb2': {   u'height': u'64',
                                                                       u'width': u'64'},
                                                  u'template': {   u'height': u'422',
                                                                   u'width': u'670'},
                                                  u'thumb': {   u'height': u'150',
                                                                u'width': u'150'}},
                          u'media_server_id': u'515f711138c2b',
                          u'media_type_id': u'0',
                          u'media_variation': [],
                          u'mimetype': u'',
                          u'modified': u'2013-04-07 08:01:08',
                          u's3': u'1',
                          u'size': u'160426',
                          u'sort': u'2',
                          u'user_id': u'35443'},
                      {   u'caption': u'',
                          u'created': u'2013-04-07 07:59:15',
                          u'extension': u'jpg',
                          u'id': u'75324',
                          u'item_id': u'16903',
                          u'jobs_remaining': u'',
                          u'media_dimension': {   u'': {   u'height': u'269',
                                                           u'width': u'190'},
                                                  u'facebook': {   u'height': u'220',
                                                                   u'width': u'150'},
                                                  u'keep_size': {   u'height': u'0',
                                                                    u'width': u'0'},
                                                  u'project_thumb': {   u'height': u'137',
                                                                        u'width': u'137'},
                                                  u'small_thumb': {   u'height': u'50',
                                                                      u'width': u'50'},
                                                  u'store_main': {   u'height': u'585',
                                                                     u'width': u'384'},
                                                  u'store_thumb': {   u'height': u'216',
                                                                      u'width': u'144'},
                                                  u'store_thumb2': {   u'height': u'64',
                                                                       u'width': u'64'},
                                                  u'template': {   u'height': u'422',
                                                                   u'width': u'670'},
                                                  u'thumb': {   u'height': u'150',
                                                                u'width': u'150'}},
                          u'media_server_id': u'51609ab30ac92',
                          u'media_type_id': u'0',
                          u'media_variation': [],
                          u'mimetype': u'',
                          u'modified': u'2013-04-07 08:01:08',
                          u's3': u'1',
                          u'size': u'203755',
                          u'sort': u'3',
                          u'user_id': u'35443'}],
        u'primary_media': {   u'caption': u'',
                              u'created': u'2013-04-06 11:49:38',
                              u'extension': u'jpg',
                              u'id': u'75308',
                              u'item_id': u'16903',
                              u'jobs_remaining': u'',
                              u'media_dimension': {   u'': {   u'height': u'269',
                                                               u'width': u'190'},
                                                      u'facebook': {   u'height': u'220',
                                                                       u'width': u'150'},
                                                      u'keep_size': {   u'height': u'0',
                                                                        u'width': u'0'},
                                                      u'project_thumb': {   u'height': u'137',
                                                                            u'width': u'137'},
                                                      u'small_thumb': {   u'height': u'50',
                                                                          u'width': u'50'},
                                                      u'store_main': {   u'height': u'585',
                                                                         u'width': u'384'},
                                                      u'store_thumb': {   u'height': u'216',
                                                                          u'width': u'144'},
                                                      u'store_thumb2': {   u'height': u'64',
                                                                           u'width': u'64'},
                                                      u'template': {   u'height': u'422',
                                                                       u'width': u'670'},
                                                      u'thumb': {   u'height': u'150',
                                                                    u'width': u'150'}},
                              u'media_server_id': u'515f71224fe59',
                              u'media_type_id': u'0',
                              u'mimetype': u'',
                              u'modified': u'2013-04-07 08:01:08',
                              u's3': u'1',
                              u'size': u'132909',
                              u'sort': u'1',
                              u'user_id': u'35443'},
        u'tag': [],
        u'variation': [   {   u'SKU': u'515F70575A91C',
                              u'UPC': u'BMJ30',
                              u'colour': u'Blue',
                              u'created': u'2013-04-06 11:48:00',
                              u'gender': u'Female',
                              u'id': u'57453',
                              u'item_id': u'16903',
                              u'location': u'EMPTY',
                              u'modified': u'2013-04-06 11:48:43',
                              u'size': u'30',
                              u'sort': u'0',
                              u'stock': u'20'},
                          {   u'SKU': u'515F706E23248',
                              u'UPC': u'BMJ32',
                              u'colour': u'Blue',
                              u'created': u'2013-04-06 11:48:10',
                              u'gender': u'Female',
                              u'id': u'57454',
                              u'item_id': u'16903',
                              u'location': u'EMPTY',
                              u'modified': u'2013-04-06 11:48:43',
                              u'size': u'32',
                              u'sort': u'1',
                              u'stock': u'15'},
                          {   u'SKU': u'515F7083615A3',
                              u'UPC': u'RMJ34',
                              u'colour': u'Red',
                              u'created': u'2013-04-06 11:48:21',
                              u'gender': u'Female',
                              u'id': u'57455',
                              u'item_id': u'16903',
                              u'location': u'EMPTY',
                              u'modified': u'2013-04-06 11:48:43',
                              u'size': u'34',
                              u'sort': u'2',
                              u'stock': u'20'},
                          {   u'SKU': u'515F70935BB16',
                              u'UPC': u'RMJ32',
                              u'colour': u'Red',
                              u'created': u'2013-04-06 11:48:32',
                              u'gender': u'Female',
                              u'id': u'57456',
                              u'item_id': u'16903',
                              u'location': u'EMPTY',
                              u'modified': u'2013-04-06 11:48:43',
                              u'size': u'32',
                              u'sort': u'3',
                              u'stock': u'15'}]}]
"""
    
