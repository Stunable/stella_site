from django.contrib import admin 
from apps.racks.models import Rack, Item, Rack_Item, Category, Size, Brand, Color, ItemType, PriceCategory

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
    

class ItemTypeInline(admin.StackedInline):
    model = ItemType
    extra = 1
    
class ItemAdmin(AdminImageMixin,admin.ModelAdmin):
    inlines = [ItemTypeInline]
    list_display = ('name','category','approved','list_image',)
    actions = ('make_pretty',)
    list_filter = ('approved',)
    search_fields = ('name','description')



    def make_pretty(self,request,queryset):
        for obj in queryset:
            obj.generate_pretty_picture()


    

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    #readonly_fields = ['retailer']
    

admin.site.register(Size, SizeAdmin)
admin.site.register(Rack)
admin.site.register(Rack_Item)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color, ColorAdmin)
admin.site.register(PriceCategory)



