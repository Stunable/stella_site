from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


import urllib2
import datetime
from bs4 import BeautifulSoup

from django.conf import settings


from apps.common.utils import OverwriteStorage

# Create your models here.
class SiteTextContent(models.Model):
    def __unicode__(self):
        return self.item_name

    item_name = models.CharField(help_text="something like this: 'a_name_with_no_spaces_or_funny_symbols'", max_length = 64)
    html = models.TextField(help_text="html tags work in this field", default="cms content placeholder", blank=True,null=True)
    component = models.CharField(help_text="what part of the site is this for?  ex:'retailers' or 'cart'",max_length=32,default='all')




class ExternalPost(models.Model):
    BLOG_TYPE_CHOICES = (
        ('blog', _('blog')),
        ('news', _('news'))
    )

    text = models.FileField(null=True,blank=True,upload_to='upload/blog_cache',storage=OverwriteStorage())
    date = models.DateField(default=datetime.datetime.now)
    post_type = models.CharField(default='news',max_length=16,choices=BLOG_TYPE_CHOICES)
    source = models.CharField(max_length=256,default=settings.EXTERNAL_CONTENT_URL['news'])
    has_content = models.BooleanField(default=False)


    def refresh_content(self):
        url = self.source + self.date.strftime('%Y/%m/%d')
        try:
            temp = NamedTemporaryFile(delete=True)
            content = urllib2.urlopen(url).read()
            print content
            temp.write(content)
            temp.flush()

            self.text.save(url.replace('/','_')+'.html', File(temp))
            self.has_content = True
            self.save()
            return True
        except Exception, e:
            print url
            print 'refresh content error:',e
            return False

    @classmethod
    def get_default_content(cls,post_type):
        post,created = ExternalPost.objects.get_or_create(date=datetime.datetime.now(),post_type=post_type)
        if created:
            if post.refresh_content():
                return post.get_content()
        else:
            if post.has_content:
                return post.get_content()

        #if we haven't returned yet, there is no post from today, so get the last one
        posts = ExternalPost.objects.filter(post_type=post_type,has_content=True).order_by('date')
        if posts:
            return posts[0].get_content()

    def get_source_url(self):
        return settings.EXTERNAL_CONTENT_URL[self.post_type]

    @property
    def post_container(self):
        return {'blog':'article','news':'div'}[self.post_type]

    def get_content(self):
        if self.text:
            html = open(settings.PROJECT_ROOT+self.text.url,'r').read()
            return [str(p) for p in BeautifulSoup(html).findAll(self.post_container, "post")]
        return []
    

@receiver(pre_save, sender=ExternalPost)
def set_source(sender,instance, **kwargs):
    instance.source = instance.get_source_url()


@receiver(post_save, sender=ExternalPost)
def updateContent(sender, instance, created, **kwargs):
    if created:
        instance.refresh_content()