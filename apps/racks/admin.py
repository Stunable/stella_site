from django.contrib import admin 
from apps.racks.models import Rack, Item, Rack_Item, Category, Size, Brand, Color, ItemType, PriceCategory,ProductImage,DailySpecial

import os
from PIL import Image

from django.db import models
from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


from django.forms.models import BaseInlineFormSet


from weekday_field.forms import WeekdayFormField,AdvancedWeekdayFormField


class AdminImageMixin(object):
    """
    This is a mix-in for ModelAdmin subclasses to make ``ImageField``
    show nicer form widget
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        # print db_field.name
        if 'image' in db_field.name:
            pass
            # return db_field.formfield(widget=AdminImageWidget)
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
    
class ItemTypeInlineFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(ItemTypeInlineFormset, self).add_fields(form, index)
        if form.instance:
            if hasattr(form.instance,'item'):
                form.fields['image'].queryset = ProductImage.objects.filter(item=form.instance.item)
            else:
                form.fields['image'].queryset = ProductImage.objects.none()

class ItemTypeInline(admin.TabularInline):
    model = ItemType
    extra = 0
    max_num = 0
    formset = ItemTypeInlineFormset
    exclude = ('api_type','object_id')

    def has_add_permission(self, request):
        return False
   


class ItemAdmin(AdminImageMixin,admin.ModelAdmin):
    inlines = [ItemTypeInline]
    list_display = ('name','category','approved','is_available','list_image','_retailer','slug')
    actions = ('approve','unapprove','set_price_text','set_item_slugs','make_featured_pretty')
    list_filter = ('approved','is_available','created_date','_retailer')
    search_fields = ('name','description')

    class Media:
        css = {
            "all": ("styles/imageselect.css",
                    "styles/admin.css",
                    'styles/smoothness/jquery-ui-1.10.2.custom.min.css'
                )
        }
        js = (
            'javascript/jquery.js',
            'javascript/jquery-ui-1.8.22.custom.min.js',
            'javascript/imageselect.js',
            "javascript/admin.js",)


    def get_form(self, request, obj=None, **kwargs):
        form = super(ItemAdmin,self).get_form(request, obj,**kwargs)
        # form class is created per request by modelform_factory function
        # so it's safe to modify
        #we modify the the queryset
        form.base_fields['featured_image'].queryset = form.base_fields['featured_image'].queryset.filter(item=obj)
        return form

    def unapprove(self,request,queryset):
        for obj in queryset:
            obj.approved = False
            obj.save()

    def approve(self,request,queryset):
        for obj in queryset:
            if obj.types.all().count():
                obj.approved = True
                obj.set_price_text()
                obj.save()

    def set_price_text(self,request,queryset):
        for obj in queryset:
            obj.set_price_text()
            obj.save()

    def make_featured_pretty(self,request,queryset):
        for obj in queryset:
            obj.set_price_text()
            obj.make_featured_pretty()
            obj.save()

    def set_item_slugs(self,request,queryset):
        for obj in queryset:
            obj.set_slug()
            obj.save()



class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('item',)
    actions = ('test_inventory_update',)
    list_per_page = 500


    def test_inventory_update(self,request,queryset):
        for obj in queryset:
            obj.update_inventory(3)

    

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    #readonly_fields = ['retailer']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image','retailer_profile','list_image']
    #readonly_fields = ['retailer']
    list_filter = ('retailer_profile',)
    search_fields = ('image','identifier')
    actions = ('make_pretty','premake_thumbs','safe_delete')

    def make_pretty(self,request,queryset):
        for obj in queryset:
            if len(queryset) == 1:
                print 'now'
                obj.generate_pretty_picture(instant=True,refresh=True)                
            else:
                obj.generate_pretty_picture(instant=False,refresh=True)

    def set_size(self,request,queryset):
        for obj in queryset:
            obj.set_size()

    def premake_thumbs(self,request,queryset):
        for obj in queryset:
            obj.get_thumbs()

    def safe_delete(self,request,queryset):
        for PI in queryset:
            if PI.item_featured_image_set.all().count() or PI.item_variation_image_set.all().count():
                return
            else:
                PI.delete()


class DailySpecialAdmin(admin.ModelAdmin):

    filter_horizontal = ('Items',)
    prepopulated_fields = {"slug": ("display_name",)}

    def formfield_for_dbfield(self, db_field, **kwargs):
        # print db_field.name
        if 'weekday' in db_field.name:
            return WeekdayFormField()
        sup = super(DailySpecialAdmin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Size, SizeAdmin)
admin.site.register(Rack)
admin.site.register(Rack_Item)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color, ColorAdmin)
admin.site.register(PriceCategory)
admin.site.register(ProductImage,ProductImageAdmin)

admin.site.register(DailySpecial,DailySpecialAdmin)



