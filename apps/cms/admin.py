from django.contrib import admin
from django import forms
from models import *




class Ext_News_Admin(admin.ModelAdmin):
    list_display = ('source','date','has_content','post_type')

    actions = ('refresh_content',)


    def refresh_content(self,request,queryset):
        for obj in queryset:
            obj.refresh_content()

admin.site.register(ExternalPost,Ext_News_Admin)
admin.site.register(SiteTextContent)