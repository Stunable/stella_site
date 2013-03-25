from django.contrib import admin 
from apps.cart.models import  Purchase, Checkout,Shipment,ShipmentTrackingEvent
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
    raw_id_fields = ("item","cart","purchaser","transaction","shipping_address")

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



class CheckoutAdmin(admin.ModelAdmin):
    list_display=('ref','complete','cart')
    raw_id_fields = ('cart','retailer','purchaser')



admin.site.register(Checkout,CheckoutAdmin)



class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('status','originator','ship_date','delivery_date','tracking_number')
    actions = ('track_shipment',)

    def track_shipment(self,request,queryset):
        for obj in queryset:
            obj.update_tracking_info()




admin.site.register(Shipment,ShipmentAdmin)
admin.site.register(ShipmentTrackingEvent)