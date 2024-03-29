from django.contrib import admin
from apps.retailers.models import *




class RetailerProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'approved')
    list_filter   = ('approved',)
    search_fields = ('name',)


admin.site.register(RetailerProfile, RetailerProfileAdmin)
 



admin.site.register(StylistItem)
admin.site.register(ShippingType)
admin.site.register(ProductUpload)

admin.site.register(ShopifyProduct)
admin.site.register(ShopifyVariation)



class APIConnectionAdmin(admin.ModelAdmin):
    actions=('refresh_all_products',)

    def refresh_all_products(self,request,queryset):
        for o in queryset:
            o.refresh_all_products()

admin.site.register(ShopifyConnection,APIConnectionAdmin)

class UploadErrorAdmin(admin.ModelAdmin):
    list_display = ('text','upload')


admin.site.register(UploadError,UploadErrorAdmin)
