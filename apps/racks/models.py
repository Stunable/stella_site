import re
import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.safestring import mark_safe
from rec_managers import RecommenderManager
from tagging.fields import TagField
from django.db.models import Avg
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.loading import get_model, get_models

from django.template.defaultfilters import slugify

from tasks import *
from apps.common.utils import *
from apps.accounts.models import AnonymousProfile

from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from queued_storage.backends import QueuedStorage
from storages.backends.s3boto import S3BotoStorage

S3BotoStorage.IGNORE_IMAGE_DIMENSIONS = False



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

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=128,null=True)
    
    def __unicode__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)
    
class ItemManager(RecommenderManager):
    pass

class Size(models.Model):
    size = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    retailer = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        return self.size
    
class DenimColorManager(models.Model):
    def get_query_set(self, *args, **kwargs):
        return super(DenimColorManager, self).get_query_set(*args, **kwargs).filter(is_denim=True)


class PlainColorManager(models.Model):
    def get_query_set(self, *args, **kwargs):
        return super(DenimColorManager, self).get_query_set(*args, **kwargs).filter(is_denim=False)


VALID_COLOR_REGEX = re.compile("^#[0-9a-fA-F]{6}$|^rgb\(\d{1,3},\d{1,3},\d{1,3}\)$")

    
    
class Color(models.Model):
    name = models.CharField(max_length=100)
    color_css = models.CharField(max_length=16,
                                 help_text='A valid CSS color in either hex (#123456) or \
                                           rgb (rgb(100,100,100) formats.')
    swatch = models.ImageField(blank=True, null=True,
                               upload_to="colors",
                               help_text="Optional Color swatch. If present, this will be \
                                         displayed instead of the plain CSS color.")
    is_denim = models.BooleanField(default=False)
    retailer = models.ForeignKey(User, blank=True, null=True)
    
    objects = models.Manager()
    plain = PlainColorManager()
    denim = DenimColorManager()
    
    def __unicode__(self):
        return self.name
    
    def clean(self):
        
        if not VALID_COLOR_REGEX.match(self.color_css):
            raise ValidationError("%s is not a valid CSS color" % self.color_css)    

class listImageMixin(object):

    @property
    def thumbnail(self):
        try:
            return self.get_image().small.url
        except:
            return 'pic'
        #get_thumbnail(self.get_image(), '120x120',  quality=100).url

    def list_image(self):
        return '<img style="width:60px" src="%s"/>' % self.thumbnail
    list_image.allow_tags = True


class ProductImage(models.Model,listImageMixin):

    def __unicode__(self):
        try:
            if self.image:
                return self.thumbnail
            else:
                return self.__class__.__name__
        except:
            self.__class__.__name__



    image = models.ImageField(upload_to='upload/%Y/%m/%d/', null=True, blank=True, verbose_name="Product Image",storage=queued_s3storage)
    pretty_image = models.ImageField(upload_to='pretty/%Y/%m/%d/', null=True, blank=True, verbose_name="Product pretty Image",storage=queued_s3storage)
    bg_color = models.CharField(max_length=32,default='white',blank=True,null=True)
    retailer = models.ForeignKey(User,null=True,blank=True)
    item = models.ForeignKey('Item',null=True, blank=True,related_name='item_image_set')

    width = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)

    tiny        = models.ImageField(upload_to='upload/t/%Y/%m/%d/', null=True, blank=True,  verbose_name="90,90",storage=queued_s3storage)
    small       = models.ImageField(upload_to='upload/s/%Y/%m/%d/', null=True, blank=True,  verbose_name="150,300",storage=queued_s3storage)
    medium      = models.ImageField(upload_to='upload/m/%Y/%m/%d/', null=True, blank=True,  verbose_name="200,400",storage=queued_s3storage)
    large       = models.ImageField(upload_to='upload/l/%Y/%m/%d/', null=True, blank=True,  verbose_name="%d,%d"%(settings.THUMB_SIZES['large'][0],settings.THUMB_SIZES['large'][1]),storage=queued_s3storage)
    extralarge  = models.ImageField(upload_to='upload/xl/%Y/%m/%d/', null=True, blank=True, verbose_name="900,1800",storage=queued_s3storage)

    identifier = models.CharField(max_length=256,blank=True,null=True)

    def orientation(self):
        if self.width>self.height:
            return 'wide'
        return 'tall'

    def color(self):
        return 'rgb%s'%self.bg_color


    def get_thumbs(self):
        for size in settings.THUMB_SIZES:
            get_thumbnail(self.pretty_image, '%dx%d'%size, crop='center', quality=99)
            # print 'thumbs for ',self,size

    def get_image(self):
        return self

    def generate_pretty_picture(self,instant=None,refresh=None):
        if instant:
            print 'prettifying',self
            prettify(self,refresh=refresh)
        else:
            print 'delayed prettify',self
            prettify.delay(self,refresh=refresh)

    def set_size(self):
        set_size(self)

    
    def image_dims(self):
        #width and height of the image are based on the large image which is 450x900
        #so... to get the width and height of the small image we would do 150/450 * w etc.
        return {
                'small': {  
                            'width' : self.width  * settings.THUMB_SIZES['small'][0]/settings.THUMB_SIZES['large'][0], 
                            'height': self.height * settings.THUMB_SIZES['small'][1]//settings.THUMB_SIZES['large'][1]
                            },
                'medium': {  
                            'width' : self.width  * settings.THUMB_SIZES['medium'][0]//settings.THUMB_SIZES['large'][0], 
                            'height': self.height * settings.THUMB_SIZES['medium'][1]//settings.THUMB_SIZES['large'][1]
                            },
                'large': {  
                            'width' : self.width,
                            'height': self.height
                            },
                'extralarge': {  
                            'width' : self.width * settings.THUMB_SIZES['extralarge'][0]//settings.THUMB_SIZES['large'][0], 
                            'height': self.height * settings.THUMB_SIZES['extralarge'][1]//settings.THUMB_SIZES['large'][1], 
                            }
            }



    def save(self,instant=None,*args,**kwargs):
        this_id = self.id
        super(ProductImage,self).save()

        if not this_id:
            self.generate_pretty_picture(instant)

    @staticmethod
    def already_exists(unique_string,retailer):
        try:
            P = ProductImage.objects.get(identifier=unique_string,retailer=retailer)
            return P
        except:
            return None


class Item(models.Model,listImageMixin):

    def get_absolute_url(self):
        return '/shop/recommendations/%s'%self.slug

    featured_image = models.ForeignKey(ProductImage,null=True,blank=True,related_name='item_featured_image_set')
    gender =         models.CharField(max_length=1,default='F',choices=[('F','F'),('M','M'),('B','B')])
    brand =          models.CharField(max_length=200, null=True, blank=True)
    name =           models.CharField(max_length=200, verbose_name='Product Name')
    price =          models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Retail Price',null=True,blank=True)
    is_onsale =      models.BooleanField(default=False, verbose_name='Currently On Sale?')
    description =    models.TextField()
    category =       models.ForeignKey(Category, verbose_name='Product Category', null=True, blank=True)
    fabrics =        models.CharField(max_length=200, null=True, blank=True)
    image_urls =     models.TextField(null=True, blank=True)
    order =          models.IntegerField(default=0, db_index=True)
    is_deleted =     models.BooleanField(default=False,blank=True)
    _retailer =      models.ForeignKey('retailers.RetailerProfile',related_name='retailer_item_set',null=True,blank=True)
    retailers =      models.ManyToManyField(User, through='retailers.StylistItem', null=True, blank=True)
    sizes =          models.ManyToManyField(Size, through='racks.ItemType', null=True, blank=True)
    colors =         models.ManyToManyField(Color,blank=True)
    created_date =   models.DateField(auto_now=True, auto_now_add=True, default=datetime.date.today)
    price_text =     models.CharField(max_length=128,default=None,blank=True,null=True)
    
    slug = models.SlugField(max_length=128,unique=True)

    approved = models.NullBooleanField(default=None)
    is_available = models.BooleanField(default=True)

    upload = models.ForeignKey('retailers.ProductUpload',null=True,blank=True)

    api_type    = models.ForeignKey(ContentType,related_name='item_api_set',null=True,blank=True)
    object_id   = models.PositiveIntegerField(null=True,blank=True)
    api_connection = generic.GenericForeignKey('api_type', 'object_id')
    
    tags = TagField()
    
    objects = ItemManager()
    
    def __unicode__(self):
        return self.name

    def make_featured_pretty(self):
        FI = self.get_image_object()
        if FI:
            FI.generate_pretty_picture(refresh=True)


    def cleanup_images(self):
        print self
        last_seen = None

        for I in self.item_image_set.all().order_by('identifier'):
            print I.identifier
            if I.identifier == last_seen:
                print '\t',last_seen
                print '\tdeleting:',I
                # I.delete()
            else:
                last_seen = I.identifier

    def get_image(self):
        return self.get_image_object()


    def get_product_images(self):
        return self.item_image_set.all()


    def get_image_object(self):
        try:
            if self.featured_image:
                print 'returning featured_image'
                return self.featured_image
            try:
                return self.item_image_set.all()[0]
            except:
                return None
        except:
            self.delete()
    
    def get_additional_images(self):
        return [im for im in self.item_image_set.all() if im.id !=self.featured_image.id]

    @property
    def retailer(self):
        if self._retailer:
            return self._retailer.name
        try:    
            RetailerProfile = get_model('retailers', 'RetailerProfile')
            return RetailerProfile.objects.filter(user=self.retailers.all()[0])[0].name
        except:
            return ''

    def get_retailer(self):
        if self._retailer:
            return self._retailer.user
        self.retailers.all()[0] 
        
    def get_full_size_image(self):
        return self.get_image()

    def price_range(self):
	seq = []
        for it in self.types.all():
             seq.extend([it.price,it.sale_price])

        if not len(seq):
            self.is_available = False
            self.save()
            return {'min':999999999,'max':999999999}


        return {'min':min(seq),'max':max(seq)}

    def price_range_text(self):
        if self.price_text and self.price_text != 'none':
            return self.price_text

        r = self.price_range()
        r.update({'sale':
            ' class="sale" ' if self.is_onsale else ''
        })
        if not r['min'] == r['max'] and self.is_onsale:
            return '<span%(sale)s><span class="dollar">$</span>%(min)s</span> - <span class="dollar">$</span>%(max)s'%r
        return '<span class="dollar">$</span>%(min)s'%r

    def total_inventory(self):
        """ returns the total inventory available of all item variations for this product"""
        return reduce(lambda x, y: x+y, [it.inventory for it in self.types.all() if it.inventory is not None], 0)

    def all_inv_in_stock(self):
        for it in self.types.all():
            if not it.inventory >= 1:
                return False
        return True

    def display_approval_status(self):
        if self.approved is False:
            return """<a href="mailto:stylists@stunable.com?subject=Why wasn't Item #%d (%s) approved?">email us</a>"""%(self.id,self.name)
        if self.approved is True:
            return 'Approved'
        return "Pending"

    def types_by_color(self):
        styles = {}
        for it in self.types.all().order_by('size'):
            if styles.has_key(it.custom_color_name):
                styles[it.custom_color_name].append(it)
            else:
                styles[it.custom_color_name] = [it]
        
        out = []
        longest = 0

        for key,val in styles.items():
            out.append(
                {
                 'color':key,
                 'list':[{'size':it.size,'inv':it.inventory,'pic':it.get_image(),'price':it.get_current_price(),'onsale':it.is_onsale} for it in val]
                }
            )
            longest = max(longest,len(val))

        return {'styles':out,'longest':longest}

    def save(self,*args,**kwargs):
        if not self.slug:
            slug = self.name
            if self._retailer:
                slug = self._retailer.name + '-' + slug

            slug = slugify(slug)
            test = slug
            i = 1
            if Item.objects.filter(slug=test).count():
                while Item.objects.filter(slug=test).exclude(id=self.id).count():
                    test = slug +'_' + str(i)
                    i += 1
            self.slug = test

        if self.total_inventory() < 1:
            self.is_available = False
        else:
            self.is_available = True

        # self.set_price_text()

        self.is_onsale = False
        for i in self.types.all():
            if i.is_onsale:
                self.is_onsale = True

        super(Item,self).save()

    def set_slug(self):
        self.slug = None


    def set_price_text(self):
        self.price_text = None
        self.price_text = self.price_range_text()
        

class ItemType(models.Model,DirtyFieldsMixin):

    class Meta:
        unique_together = (('item', 'size','custom_color_name'))

    image = models.ForeignKey(ProductImage,null=True,blank=True)
    item = models.ForeignKey('Item', related_name='types')
    size = models.ForeignKey('Size',default=1)
    SKU = models.CharField(max_length=64,null=True,blank=True)
    custom_color_name = models.CharField(max_length=100, 
                                         help_text="An optional name for the color of this item",verbose_name="Style Name")
    position = models.IntegerField(default=0,blank=True,null=True)

    inventory = models.PositiveIntegerField(default=None,null=True,verbose_name="inventory quantity")
    price = models.DecimalField(blank=True,null=True,max_digits=19, decimal_places=2, verbose_name='Special Price for this color/size/inventory')
    
    is_onsale = models.BooleanField(default=False, verbose_name='Currently On Sale?')
    sale_price = models.DecimalField(blank=True,null=True,max_digits=19, decimal_places=2, verbose_name='Sale Price for this color/size/inventory')

    api_type    = models.ForeignKey(ContentType,related_name='variation_api_set',null=True,blank=True)
    object_id       = models.PositiveIntegerField(null=True,blank=True)
    api_connection  = generic.GenericForeignKey('api_type', 'object_id')

    def get_image(self):
        img = self.image
        if img:
            return img
        else:
            return self.item.get_image()

    def get_image_id(self):
        if self.image:
            return self.image.id
        return None
    
    def get_current_price(self):
        if self.is_onsale:
            return self.sale_price
        return self.price


    def __unicode__(self):
        color = self.custom_color_name
        return "%s %s, Size %s" % (color, self.item.name, self.size.size)


    @property
    def color(self):
        return Color(name=self.custom_color_name)

@receiver(post_save, sender=ItemType,dispatch_uid="item_type_post_inventorySave")
def postSaveGeneric(sender, instance, created, **kwargs):
    dks = instance.get_dirty_fields().keys()

    if 'inventory' in dks and not created and instance._original_state['inventory'] is not None:
        if instance.api_connection:
            instance.api_connection.update_inventory(instance.inventory)
        instance.item.save()

    if 'is_onsale' in instance.get_dirty_fields().keys():
        instance.item.save()

class RackManager(models.Manager):
        
    def RacksSharedWithUser(self, user):
        return Rack.objects.filter(shared_users__username__contains=user)
    
    def SharedRacksForUser(self, user):
        user_racks = Rack.objects.filter(user=user)
        shared_racks = []
        for rack in user_racks:
            if rack.shared_users.all() or rack.publicity == Rack.PUBLIC:
                shared_racks.append(rack)
        return shared_racks
    
    def PublicRacksForUser(self, user):
        public_rack = Rack.objects.filter(publicity=Rack.PUBLIC, user=user)
        return public_rack;
    
    def PrivateRacksForUser(self, user):
        user_racks = Rack.objects.filter(user=user)
        private_racks = []
        for rack in user_racks:
#            if not rack.shared_users.all() and rack.publicity == Rack.PRIVATE:
            # new logic for private rack
            if rack.publicity == Rack.PRIVATE:
                private_racks.append(rack)
        # # get shared racks for current user too
        # shared_racks = Rack.objects.filter(shared_users__in = [user])
        # for rack in shared_racks:
        #     private_racks.append(rack)
        
        return private_racks
    
    def OwnedRacksForUser(self, user):
        user_racks = Rack.objects.filter(user=user,publicity=0)
        return user_racks
    
class Rack(models.Model):
    PRIVATE = 0
    PUBLIC = 1
    #SHARED = 2
    
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="owned_by_user", null=True, blank=True)
    anon_user_profile = models.ForeignKey(AnonymousProfile, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    shared_users = models.ManyToManyField(User, related_name="shared_users", null=True, blank=True)
    rack_items = models.ManyToManyField(Item, through='Rack_Item')
    publicity = models.SmallIntegerField(null=True, blank=True)

    objects = RackManager()
    
    def __unicode__(self):
        return self.name
    
    def get_rack_items(self):
        return self.rack_items.all()
    
    def get_shared_users(self):
        return self.shared_users.all()
    
    def delete(self):
        """
        prevent not authorized user delete this rack
        """
        return super(Rack, self).delete()
    
    def is_public(self):
        return self.publicity == Rack.PUBLIC

    def get_owner(self):
        if self.user:
            return self.user
        if self.anon_user_profile:
            return self.anon_user_profile

    def set_owner(self, owner):
        if 'AnonymousProfile' in str(owner.__class__):
            self.anon_user_profile = owner
        else:
            self.user = owner.user
        #self.save()

    owner = property(get_owner, set_owner)

    
class Rack_Item(models.Model):
    item = models.ForeignKey(Item)
    rack = models.ForeignKey(Rack)
    user = models.ForeignKey(User, null=True, blank=True)
    created_date = models.DateField(auto_now=True, auto_now_add=True, default=datetime.date.today)
    
    def __unicode__(self):
        return self.rack.name + ' ' + self.item.name

class PriceCategory(models.Model):
    name = models.CharField(max_length=200)
    display_value = models.CharField(max_length=200, help_text="The string value of price range that will be displayed")
    min_price = models.FloatField(blank=True, null=True)
    max_price = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return self.display_value

class Brand(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    category = models.ForeignKey(PriceCategory, blank=True, null=True)
            
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_product_group_from_brand(cls, brand_name):
        res = Item.objects.all().filter(brand__iexact=brand_name).aggregate(Avg('price'))
        avg_price = res['price__avg']
        for (group, (vmin, vmax)) in settings.PRODUCT_GROUPS.items():
            if avg_price > vmin and avg_price < vmax:
                return group
