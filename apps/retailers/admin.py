from django.contrib import admin
from apps.retailers.models import *

from apps.common.admin import NotificationSender



class RetailerProfileAdmin(admin.ModelAdmin,NotificationSender):
    list_display  = ('name', 'approved','admin_link')
    list_filter   = ('approved',)
    search_fields = ('name',)
    actions = ('verify_address','send_notifications')
    


admin.site.register(RetailerProfile, RetailerProfileAdmin)
 

class ProductUploadAdmin(admin.ModelAdmin,NotificationSender):
    actions = ('send_notifications',)


admin.site.register(StylistItem)
admin.site.register(ShippingType)
admin.site.register(ProductUpload,ProductUploadAdmin)
admin.site.register(ShopifyProduct)
admin.site.register(ShopifyVariation)
admin.site.register(PortableProduct)
admin.site.register(PortableVariation)



class APIConnectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','retailer_profile','last_updated',)
    actions=('refresh_all_products','test_auth')

    def refresh_all_products(self,request,queryset):
        for o in queryset:
            o.refresh_all_products()

    def test_auth(self,request,queryset):
        for o in queryset:
            o.authenticate()

admin.site.register(ShopifyConnection,APIConnectionAdmin)

admin.site.register(PortableConnection,APIConnectionAdmin)

class UploadErrorAdmin(admin.ModelAdmin):
    list_display = ('text','upload')


admin.site.register(UploadError,UploadErrorAdmin)
