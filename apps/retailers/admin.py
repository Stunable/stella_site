from django.contrib import admin
from apps.retailers.models import RetailerProfile, StylistItem, ShippingType

admin.site.register(RetailerProfile)
admin.site.register(StylistItem)
admin.site.register(ShippingType)