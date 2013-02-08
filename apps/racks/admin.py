from django.contrib import admin 
from apps.racks.models import Rack, Item, Rack_Item, Category, Size, Brand, Color, ItemType, PriceCategory,ProductImage

import os
from PIL import Image

from django.db import models
from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


__all__ = ['AdminImageWidget', 'AdminImageMixin']


get_thumbnail = None

try:
    from easy_thumbnails.files import get_thumbnailer
except ImportError:
    def thumbnail1(image_path):
        absolute_url = os.path.join(settings.MEDIA_URL, image_path)
        return u'<img src="%s" alt="" width="160" />' % absolute_url
    get_thumbnail = thumbnail1
else:
    def thumbnail2(image_path):
        thumbnailer = get_thumbnailer(image_path)
        thumbnail_options = {
            'crop': True, 'size': (160, 120), 'detail': True, 'upscale': True}
        t = thumbnailer.get_thumbnail(thumbnail_options)
        media_url = settings.MEDIA_URL
        return u'<img src="%s%s" alt="" width="160" height="120"/>' % (
            media_url, t)
    get_thumbnail = thumbnail2


class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = ''.join((settings.MEDIA_URL, file_name))
            try:
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
            except IOError:
                # Not an image
                output.append('%s <a target="_blank" href="%s">%s</a> '
                              '<br />%s ' % (_('Currently:'), file_path,
                                             file_name, _('Change:')))
            else:
                output.append('<a target="_blank" href="%s">%s</a>' % (
                              file_path, get_thumbnail(file_name)))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class AdminImageMixin(object):
    """
    This is a mix-in for ModelAdmin subclasses to make ``ImageField``
    show nicer form widget
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.ImageField):
            print db_field
            return db_field.formfield(widget=AdminImageWidget)
        sup = super(AdminImageMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)


class ColorAdmin(admin.ModelAdmin):
    list_filter = ['is_denim']
    list_display = ['name', 'color_css']
    
    def queryset(self, request):
        # Force the admin to not use one of the custom managers
        qs = self.model.objects.get_query_set()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
    

class ItemTypeInline(admin.TabularInline):
    model = ItemType
    extra = 0
    
class ItemAdmin(AdminImageMixin,admin.ModelAdmin):
    inlines = [ItemTypeInline]
    list_display = ('name','category','approved','is_available','list_image','_retailer','slug')
    actions = ('approve','unapprove','set_price_text','set_item_slugs')
    list_filter = ('approved','is_available','created_date','_retailer')
    search_fields = ('name','description')

    def unapprove(self,request,queryset):
        for obj in queryset:
            obj.approved = False
            obj.save()

    def approve(self,request,queryset):
        for obj in queryset:
            if obj.types.all().count():
                obj.approved = True
                obj.save()

    def set_price_text(self,request,queryset):
        for obj in queryset:
            # obj.set_price_text()
            obj.save()


    def make_pretty(self,request,queryset):
        for obj in queryset:
            obj.generate_pretty_picture()

    def set_item_slugs(self,request,queryset):
        for obj in queryset:
            obj.set_slug()
            obj.save()




    

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    #readonly_fields = ['retailer']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image','retailer','list_image']
    #readonly_fields = ['retailer']
    list_filter = ('retailer',)
    search_fields = ('name','description','item')
    actions = ('make_pretty','premake_thumbs')

    def make_pretty(self,request,queryset):
        for obj in queryset:
            obj.generate_pretty_picture()

    def set_size(self,request,queryset):
        for obj in queryset:
            obj.set_size()

    def premake_thumbs(self,request,queryset):
        for obj in queryset:
            obj.get_thumbs()


    

admin.site.register(Size, SizeAdmin)
admin.site.register(Rack)
admin.site.register(Rack_Item)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color, ColorAdmin)
admin.site.register(PriceCategory)
admin.site.register(ProductImage,ProductImageAdmin)



