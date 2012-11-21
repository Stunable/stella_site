from django.contrib import admin
from apps.retailers.models import RetailerProfile, StylistItem, ShippingType, ProductUpload




class RetailerProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'approved')
    list_filter   = ('approved',)
    search_fields = ('name',)


admin.site.register(RetailerProfile, RetailerProfileAdmin)
 



admin.site.register(StylistItem)
admin.site.register(ShippingType)
admin.site.register(ProductUpload)
