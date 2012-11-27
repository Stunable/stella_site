from django.contrib import admin 
from apps.cart.models import Cart, Purchase, Checkout,Item,ShippingLabel
from plugins.track_shipment import track_it
class CartAdmin(admin.ModelAdmin):
    list_display=('__unicode__','checked_out','ref','grand_total')

admin.site.register(Cart,CartAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=('cart','checkout','transaction_status','item','shipping_number','delivery_date')
    actions = ('track_package','capture_payment')

    def transaction_status(self,instance):
        return instance.transaction.state

    def capture_payment(self,request,queryset):
        for obj in queryset:
            obj.transaction.capture_funds()

    def track_package(self,request,queryset):
        for obj in queryset:
            if obj.shipping_number:
                try:
                    track_it(obj.shipping_number)
                except Exception,e:
                    print e


admin.site.register(Purchase,PurchaseAdmin)



class PurchaseInline(admin.TabularInline):
    model = Purchase
    #exclude = ('orientation',)
    #readonly_fields = ('cart')


class CheckoutAdmin(admin.ModelAdmin):
    list_display=('ref','complete','cart')

    inlines = [PurchaseInline]



admin.site.register(Checkout,CheckoutAdmin)


admin.site.register(Item)
admin.site.register(ShippingLabel)