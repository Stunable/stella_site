from django.contrib import admin
from apps.retailers.models import RetailerProfile, StylistItem, ShippingType, ProductUpload,UploadError,ShopifyProduct




class RetailerProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'approved')
    list_filter   = ('approved',)
    search_fields = ('name',)


admin.site.register(RetailerProfile, RetailerProfileAdmin)
 



admin.site.register(StylistItem)
admin.site.register(ShippingType)
admin.site.register(ProductUpload)
admin.site.register(ShopifyProduct)

class UploadErrorAdmin(admin.ModelAdmin):
    list_display = ('text','upload')


admin.site.register(UploadError,UploadErrorAdmin)
