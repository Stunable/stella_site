from django.contrib import admin
from apps.retailers.models import *




class RetailerProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'approved','admin_link')
    list_filter   = ('approved',)
    search_fields = ('name',)
    actions = ('verify_address',)
    


admin.site.register(RetailerProfile, RetailerProfileAdmin)
 



admin.site.register(StylistItem)
admin.site.register(ShippingType)
admin.site.register(ProductUpload)

# admin.site.register(ShopifyProduct)
# admin.site.register(ShopifyVariation)



class APIConnectionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','last_updated',)
    actions=('refresh_all_products',)

    def refresh_all_products(self,request,queryset):
        for o in queryset:
            o.refresh_all_products()

admin.site.register(ShopifyConnection,APIConnectionAdmin)

admin.site.register(PortableConnection,APIConnectionAdmin)

class UploadErrorAdmin(admin.ModelAdmin):
    list_display = ('text','upload')


admin.site.register(UploadError,UploadErrorAdmin)
