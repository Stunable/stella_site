from django.contrib import admin 
from apps.cart.models import  Purchase, Checkout,Shipment
from apps.kart.models import Kart,KartItem,WishListItem
from plugins.track_shipment import track_it
class CartAdmin(admin.ModelAdmin):
    list_display=('__unicode__','checked_out','ref','grand_total','creation_date')

admin.site.register(Kart,CartAdmin)



class WishlistItemAdmin(admin.ModelAdmin):
    raw_id_fields = ('item_variation','item','picture','user')


class KartItemAdmin(admin.ModelAdmin):
    raw_id_fields = ('item_variation','kart')

admin.site.register(KartItem,KartItemAdmin)
admin.site.register(WishListItem,WishlistItemAdmin)



class PurchaseAdmin(admin.ModelAdmin):
    list_display=('cart','item','status','last_tracking_number','delivery_date','transaction_status')
    actions = ('track_package','check_payment_status','capture_payment')
    list_filter=('status',)
    raw_id_fields = ("item","cart")

    def transaction_status(self,instance):
        return instance.transaction.state

    def check_payment_status(self,request,queryset):
        for obj in queryset:
            obj.transaction.get_status()

    def capture_payment(self,request,queryset):
        for obj in queryset:
            obj.transaction.capture_funds()

    def track_package(self,request,queryset):
        for obj in queryset:
            if obj.last_tracking_number:
                try:
                    delivery_date = track_it(obj.last_tracking_number)
                    if delivery_date:
                        obj.delivery_date = delivery_date
                        obj.save()
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

admin.site.register(Shipment)