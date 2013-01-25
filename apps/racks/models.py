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

from sorl.thumbnail import ImageField,get_thumbnail

from django.template.defaultfilters import slugify

from tasks import *
from apps.common.utils import *
from apps.accounts.models import AnonymousProfile

from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
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
            return self.get_image().url
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


    image = ImageField(upload_to='upload/%Y/%m/%d/', null=True, blank=True, verbose_name="Product Image")
    pretty_image = models.ImageField(upload_to='upload/%Y/%m/%d/', null=True, blank=True, verbose_name="Product pretty Image",storage=OverwriteStorage())
    bg_color = models.CharField(max_length=32,default='white',blank=True,null=True)
    retailer = models.ForeignKey(User,null=True,blank=True)
    item = models.ForeignKey('Item',null=True, blank=True,related_name='item_image_set')

    identifier = models.CharField(max_length=256,blank=True,null=True)

    def get_image(self):
        if self.pretty_image:
            return self.pretty_image
        else:
            return self.image

    def generate_pretty_picture(self):
        prettify(self)

    def save(self,*args,**kwargs):
        this_id = self.id
        super(ProductImage,self).save()

        if not this_id:
            self.generate_pretty_picture()

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
    gender = models.CharField(max_length=1,default='F',choices=[('F','F'),('M','M'),('B','B')])
    brand = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Product Name')
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Retail Price',null=True,blank=True)
    is_onsale = models.BooleanField(default=False, verbose_name='Currently On Sale?')
    description = models.TextField()
    category = models.ForeignKey(Category, verbose_name='Product Category', null=True, blank=True)
    fabrics = models.CharField(max_length=200, null=True, blank=True)
    image_urls = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0, db_index=True)
    is_deleted = models.BooleanField(default=False,blank=True)
    _retailer = models.ForeignKey('retailers.RetailerProfile',related_name='retailer_item_set',null=True,blank=True)
    retailers = models.ManyToManyField(User, through='retailers.StylistItem', null=True, blank=True)
    sizes = models.ManyToManyField(Size, through='racks.ItemType', null=True, blank=True)
    colors = models.ManyToManyField(Color,blank=True)
    created_date = models.DateField(auto_now=True, auto_now_add=True, default=datetime.date.today)
    
    slug = models.SlugField()

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
    
    def get_image(self):
        if self.featured_image:
            if self.featured_image.pretty_image:
                return self.featured_image.pretty_image
        if self.featured_image:
            return self.featured_image.image
        elif self.image_urls:
            return self.image_urls.split(',')[0].replace('.jpg', '_150x296.jpg')
        else:
            return None
#            return "%simages/general/agjea1.254x500.jpg" % (settings.STATIC_URL)
    
    def get_additional_images(self):
        return [im for im in self.item_image_set.all() if im !=self.featured_image]

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
        if self.featured_image:
            return self.featured_image.image
        elif self.image_urls:
            return self.image_urls.split(',')[0]
        else: 
            return None

    def price_range(self):
        seq = [it.get_current_price() for it in self.types.all()]
        if not len(seq):
            return
        return {'min':min(seq),'max':max(seq)}

    def price_range_text(self):
        r = self.price_range()
        r.update({'sale':
            ' class="sale" ' if self.is_onsale else ''
        })

        print r
        if not r['min'] == r['max']:
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
            self.slug = slug

        if self.total_inventory() < 1:
            self.is_available = False
        else:
            self.is_available = True

        self.is_onsale = False
        for i in self.types.all():
            if i.is_onsale:
                self.is_onsale = True


        super(Item,self).save()

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
        if self.image:
            return self.image.image
        else:
            return self.item.get_image()
    
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