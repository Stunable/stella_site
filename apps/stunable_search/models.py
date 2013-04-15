from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

class Flavor(models.Model):
    name  = models.CharField(max_length = 64)
    group = models.CharField('a name for a group of flavors like "mood", "occasion", "color"',max_length = 64,blank=True,null=True)

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