from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

from apps.news.managers import PublicManager
from apps.common.utils import OverwriteStorage


import datetime
import tagging
from tagging.fields import TagField

import urllib2


class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'news_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('news_category_detail', None, {'slug': self.slug})


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, related_name="news_author", blank=True, null=True)
    body = models.TextField(_('body'), )
    tease = models.TextField(_('tease'), blank=True, help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = TagField()
    objects = PublicManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table  = 'news_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('news_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)


class ExternalPost(models.Model):
    BLOG_TYPE_CHOICES = (
        ('blog', _('blog')),
        ('news', _('news'))
    )

    text = models.FileField(null=True,blank=True,upload_to='upload/blog_cache',storage=OverwriteStorage())
    date = models.DateField(default=datetime.datetime.now)
    post_type = models.CharField(default='news',max_length=16,choices=BLOG_TYPE_CHOICES)
    source = models.CharField(max_length=256,default=settings.EXTERNAL_NEWS_BLOG_URL)


    def refresh_content(self):
        url = self.source + self.date.strftime('%Y/%m/%d')
        try:
            temp = NamedTemporaryFile(delete=True)
            temp.write(urllib2.urlopen(url).read())
            temp.flush()

            self.text.save(url.replace('/','_')+'.html', File(temp))
        except Exception, e:
            print e

@receiver(post_save, sender=ExternalPost)
def updateContent(sender, instance, created, **kwargs):
    if not instance.text:
        instance.refresh_content()






