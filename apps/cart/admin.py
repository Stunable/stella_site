from django.contrib import admin 
from apps.cart.models import Cart, Purchase, Checkout,Item,ShippingLabel


class CartAdmin(admin.ModelAdmin):
    list_display=('__unicode__','checked_out','ref','grand_total')

admin.site.register(Cart,CartAdmin)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=('cart','checkout','transaction_status')

    def transaction_status(self,instance):
        return instance.transaction.state

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