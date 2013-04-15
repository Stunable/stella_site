from django.contrib import admin 

from models import *


class FlavorAdmin(admin.ModelAdmin):

    filter_horizontal = ('Tags',)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)

    

admin.site.register(Flavor,FlavorAdmin)