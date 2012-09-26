from django.contrib import admin 
from apps.racks.models import Rack, Item, Rack_Item, Category, Size, Brand, Color, ItemType, PriceCategory

class ColorAdmin(admin.ModelAdmin):
    list_filter = ['is_denim']
    list_display = ['name', 'color_css']
    
    def queryset(self, request):
        # Force the admin to not use one of the custom managers
        qs = self.model.objects.get_query_set()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
    

class ItemTypeInline(admin.StackedInline):
    model = ItemType
    extra = 1
    
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemTypeInline]

    actions = ('make_pretty',)

    def make_pretty(self,request,queryset):
        for obj in queryset:
            obj.generate_pretty_picture()
    

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    #readonly_fields = ['retailer']
    

admin.site.register(Size, SizeAdmin)
admin.site.register(Rack)
admin.site.register(Rack_Item)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color, ColorAdmin)
admin.site.register(PriceCategory)