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

from django.template.defaultfilters import slugify

from apps.shopping_platforms.models import APIPlatformConnection,APIProductConnection
from shopping_platforms.tasks import update_API_products

import apps.portable as portable


from apps.common.forms import FedexTestAddress

from tasks import process_upload,save_shopify_inventory_update

from queued_storage.backends import QueuedStorage
from storages.backends.s3boto import S3BotoStorage


if settings.DEBUG:
    queued_s3storage = QueuedStorage(
        'django.core.files.storage.FileSystemStorage',
        'django.core.files.storage.FileSystemStorage',
        # 'storages.backends.s3boto.S3BotoStorage'
        )
else:
    queued_s3storage = QueuedStorage(
    'django.core.files.storage.FileSystemStorage',
    'storages.backends.s3boto.S3BotoStorage'
    )   

def get_retailer_profile(request,retailer_id=None):
    try:
        if request.user.is_authenticated():
            try:
                return RetailerProfile.objects.filter(user=request.user)[0]
            except Exception,e:
                print e
                print 'no retailer for logged in user',request.user
                pass
        if request.session.get('active_retailer_profile',None):
            print 'found session retailer:',request.session.get('active_retailer_profile')
            return request.session.get('active_retailer_profile')
        if retailer_id:
            return RetailerProfile.objects.get(id=retailer_id)
        if request.user.is_staff:
            return RetailerProfile.objects.get(id=request.GET.get('retailer',None))
    except:
        print 'could not find retailer profile for ',request.user
        return None


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


    search_group_name = 'brand'


    name = models.CharField(max_length=255,null=True,default='')
    user = models.ForeignKey(User, blank=True, null=True)
    address1 = models.CharField(max_length=255, null=True,blank=True)
    address2 = models.CharField(max_length=255, null=True,blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, choices=US_STATES,null=True,blank=True)
    zip_code = models.CharField(max_length=10,null=True,blank=True)
    hours = models.CharField(max_length=50, null=True, blank=True)
    phone_number = PhoneNumberField(null=True,blank=True)
    email_address = models.EmailField(null=True)
    company_logo = models.ImageField(upload_to='upload',null=True,blank=True,storage=queued_s3storage)
    description = models.TextField(null=True)
    selling_options = models.CharField(max_length=100,null=True,blank=True)
    more_details = models.CharField(max_length=100, blank=True, null=True)
    wepay_acct = models.CharField(max_length=64,null=True,blank=True)
    wepay_token = models.CharField(max_length=128,null=True,blank=True)
    shipping_type = models.ManyToManyField(ShippingType, null=True, blank=True)
    accept_refund = models.BooleanField(default=False)
    welcome_message_sent = models.BooleanField(default=False)
    not_accept_refund = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    slug = models.SlugField(blank=True)
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
        return self.company_logo or "media/upload/default_avatar.gif"
        
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)

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
                
#                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [self.email_address])
                send_mail(subject, email_message, settings.EMAIL_HOST_USER, [self.email_address])
                subject = "NEW RETAILER:%s"%self.name
                email_message = "THE FOLLOWING EMAIL WAS SENT TO %s\n"%self.email_address + email_message
                send_mail(subject, email_message, settings.EMAIL_HOST_USER, [settings.RETAILER_EMAIL])
        try:
            if self.email_address:
                new_user = User.objects.get(username=self.email_address)
                new_user.is_active = True
                new_user.save()
                self.user = new_user

                for obj in self.retailer_item_set.all():
                    obj.set_slug()
                    obj.save()

        except User.DoesNotExist:
            pass                    
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


    def get_APIs(self):
        return APIConnection.objects.filter(retailer_profile=self).select_related('ShopifyConnection','PortableConnection')



class StylistItem(models.Model):
    stylist = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    
    def __unicode__(self):
        try:
            return self.stylist.username + ' ' + self.item.name
        except:
            return '-deleted- '


            

class ShopifyProduct(APIProductConnection):
    pass

    
class ShopifyVariation(APIProductConnection):

    def update_inventory(self,item_variation,number_sold):

        save_shopify_inventory_update.delay(self.api_connection.shopifyconnection,self.source_id,item_variation,number_sold)    


class APIConnection(APIPlatformConnection):
    
    def get_child(self):
        for api_type in ['shopifyconnection','portableconnection']:
            if hasattr(self,api_type):
                return getattr(self,api_type)

    @classmethod
    def get_or_create_from_request(cls,request):

        retailer = get_retailer_profile(request)
        connection = None

        if not retailer:
            try:
                connection = cls.objects.get(access_token=request.POST.get('access_token'))
                retailer = connection.retailer_profile
                return connection,retailer
            except:
            #we will only get to this if there is no existing connection for this access token
                retailer = RetailerProfile.objects.create()


        connection,created = cls.objects.get_or_create(access_token=request.POST.get('access_token'),retailer_profile=retailer)
        # request.session['active_retailer_profile'] = retailer
        # if connection.authenticate():
        update_API_products(connection)
        return connection,retailer
        # else:
            # return connection,retailer


class ShopifyConnection(APIConnection):

    logo = 'images/shopify_button.png'
    name = 'Shopify'

    def __unicode__(self):
        return self.shop_url

    ITEM_API_CLASS = ShopifyProduct
    VARIATION_API_CLASS = ShopifyVariation
    
    # these probably won't need to change
    SIZE_CLASS = Size
    ITEM_TYPE_CLASS = ItemType
    ITEM_CLASS = Item
    IMAGE_CLASS = ProductImage

    shop_url = models.TextField()
    access_token = models.TextField()

    
    variants_Have_Prices = True

    def authenticate(self):
        try:
            return self.get_session().Shop.current().to_dict()['email']
        except:
            raise
            return False


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
                    'position':'position'
                }
            }

        }
        for o in pd['options']:
            if o['name'] in ['size','Size','Chain Lengh',]:
                out['itemtype']['fields']['size'] = 'option'+str(o['position'])
            for n in ['color', 'style','material','frame','gemstone','title']:
                if n in o['name'].lower():
                    out['itemtype']['fields']['custom_color_name'] = 'option'+str(o['position'])
                    continue

        if not out['itemtype']['fields'].get('custom_color_name',None) and not out['itemtype']['fields'].get('size',None):
            # print "COULD NOT FIND COLOR OR SIZE IN:",pd['options']
            pass
        return out

    @staticmethod
    def get_id(pd):
        return pd['id']

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

    @staticmethod
    def get_name(product_dict):
        return product_dict['title']

    @staticmethod
    def get_brand(product_dict):
        return product_dict['vendor']

    @staticmethod
    def get_prices(variation_object):
        """ shopify variants don't always have a "compare at price" so we need to handle that"""

        sale_price = variation_object['price']
        price = sale_price

        if variation_object['compare_at_price']:
            price = variation_object['compare_at_price']

        return price,sale_price



class PortableProduct(APIProductConnection):
    pass

    
class PortableVariation(APIProductConnection):
    pass


class PortableConnection(APIConnection):

    logo = 'images/portableshops_button.png'
    name = 'Portable Shops'

    def __unicode__(self):
        return self.api_url+self.access_token

    ITEM_API_CLASS = PortableProduct
    VARIATION_API_CLASS = PortableVariation

    SIZE_CLASS = Size
    ITEM_TYPE_CLASS = ItemType
    ITEM_CLASS = Item
    IMAGE_CLASS = ProductImage

    api_url = 'https://api.portableshops.com/'
    access_token = models.CharField(max_length=64,null=True)

    variants_Have_Prices = False

    def authenticate(self):
        api = portable.ShoppingPlatformAPI(self)
        T = api.test_authenticate()
        return T

    def get_products(self):
        api = portable.ShoppingPlatformAPI(self)

        l = api.extract_product_list()
        return api.extract_product_list()

    def get_variations(self,product_dict):
        return product_dict['variation']

    @staticmethod
    def get_full_size_media_path(data):
        out = [data['media_server_id']]
        out.extend(
            [
                data['media_dimension']['template']['width'],
                data['media_dimension']['template']['height'],
                data['extension']
            ]
        )

        return '.'.join(out)

    def get_images(self,pd):
        path = 'http://images.portableshops.com/'
        yield path+ self.get_full_size_media_path(pd['primary_media']),pd['primary_media']['id']
        for img in pd['media']:
            yield path+ self.get_full_size_media_path(img),img['id']

    @staticmethod
    def get_id(pd):
        return pd['item']['id']

    @staticmethod
    def get_description(pd):
        return pd['item']['description']
       
    @staticmethod
    def field_mapping(pd):
        out = {
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
                    'SKU':'UPC',
                    'inventory':'stock',
                    'position':'sort',
                    'size':'size',
                    'custom_color_name':'colour'
                }
            }

        }

        return out

    @staticmethod
    def get_prices(pd):
        return float(pd['item']['price'])/100,float(pd['item']['sale_price'])/100

    @staticmethod
    def get_name(product_dict):
        return product_dict['item']['name']

    @staticmethod
    def get_brand(product_dict):
        return product_dict['item']['designer_name']
