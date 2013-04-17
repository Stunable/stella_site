from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
# Create your models here.

class Flavor(models.Model):

    def __unicode__(self):
        return self.group + '-' + self.name
    name  = models.CharField(max_length = 64)
    group = models.CharField('group name',max_length = 64,blank=True,null=True)

    slug = models.SlugField()
    Tags = models.ManyToManyField('tagging.Tag')
    Flavor = models.ForeignKey('Flavor',null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    # picture = models.ImageField(blank=True,null=True,)


    def save(self,*args,**kwargs):
        # if not self.slug:
        self.slug = slugify(self.name)
        super(Flavor,self).save(*args,**kwargs) 


    def get_contained_tags(self):
        return self.Tags.all()

    @property
    def search_group_name(self):
        return self.group


class UserSearchTab(models.Model):

    def __unicode__(self):
        return self.group + '-' + self.name

    can_be_removed = True

    group = models.CharField(max_length = 64,blank=True)
    slug = models.SlugField(blank=True)
    name = models.CharField(max_length = 200,blank=True,null=True)

    is_default = models.BooleanField(default=False)
    users = models.ManyToManyField(User,blank=True)

    # these should not be queried, they are only for diagnostic/testing/dev
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    original_object = generic.GenericForeignKey('content_type', 'object_id')


    def save(self,*args,**kwargs):
        obj = self.original_object

        self.slug = obj.slug
        self.group = obj.search_group_name
        self.name = obj.name

        super(UserSearchTab,self).save(*args,**kwargs)