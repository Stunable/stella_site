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
from django.db.models.loading import get_model, get_models

from tasks import *
from apps.common.utils import *
from apps.accounts.models import AnonymousProfile

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

class Item(models.Model):
    image = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name="Product Image")
    pretty_image = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name="Product pretty Image",storage=OverwriteStorage())
    bg_color = models.CharField(max_length=32,default='white',blank=True,null=True)

    brand = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Product Name')
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Retail Price')
    is_onsale = models.BooleanField(default=False, verbose_name='Currently On Sale?')
    description = models.TextField()
    category = models.ForeignKey(Category, verbose_name='Product Category', null=True, blank=True)
    fabrics = models.CharField(max_length=200, null=True, blank=True)
    image_urls = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0, db_index=True)
    is_deleted = models.BooleanField(default=False,blank=True)
    
    retailers = models.ManyToManyField(User, through='retailers.StylistItem', null=True, blank=True)
    sizes = models.ManyToManyField(Size, through='racks.ItemType', null=True, blank=True)
    colors = models.ManyToManyField(Color, through='racks.ItemType', null=True, blank=True)
    created_date = models.DateField(auto_now=True, auto_now_add=True, default=datetime.date.today)
    
    approved = models.BooleanField(default=False)
    
    tags = TagField()
    
    objects = ItemManager()
    
    def __unicode__(self):
        return self.name
    
    def get_image(self):
        if self.pretty_image:
            return self.pretty_image
        if self.image:
            return self.image
        elif self.image_urls:
            return self.image_urls.split(',')[0].replace('.jpg', '_150x296.jpg')
        else:
            return "upload/agjea1.254x500.jpg"
#            return "%simages/general/agjea1.254x500.jpg" % (settings.STATIC_URL)
        
    def retailer(self):
        try:    
            RetailerProfile = get_model('retailers', 'RetailerProfile')
            return RetailerProfile.objects.filter(user=self.retailers.all()[0])[0].name
        except:
            return ''
        
    def get_full_size_image(self):
        if self.image:
            return self.image
        elif self.image_urls:
            return self.image_urls.split(',')[0]
        else: 
            return "upload/agjea1.254x500.jpg"

    def generate_pretty_picture(self):
        prettify(self)


    def list_image(self):
        return '<img style="width:60px" src="/media/%s"/>' % self.get_image()
    list_image.allow_tags = True



class ItemType(models.Model):
    item = models.ForeignKey('Item', related_name='types')
    color = models.ForeignKey('Color')
    size = models.ForeignKey('Size')
    custom_color_name = models.CharField(max_length=100, blank=True, null=True,
                                         help_text="An optional custom name for the color of this item")
    inventory = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        color = self.custom_color_name or self.color.name
        return "%s %s, Size %s" % (color, self.item.name, self.size.size)
    

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
        # get shared racks for current user too
        shared_racks = Rack.objects.filter(shared_users__in = [user])
        for rack in shared_racks:
            private_racks.append(rack)
        
        return private_racks
    
    def OwnedRacksForUser(self, user):
        user_racks = Rack.objects.filter(user=user)
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