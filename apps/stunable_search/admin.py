from django.contrib import admin 

from models import *


class FlavorAdmin(admin.ModelAdmin):

    filter_horizontal = ('Tags',)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','group')
    list_filter = ('group',)

    



class SearchTabAdmin(admin.ModelAdmin):

	readonly_fields = ('group','name','slug')

	class Media:
	        css = {
	            "all": ("styles/imageselect.css",
	                    "styles/admin.css",
	                    'styles/smoothness/jquery-ui-1.10.2.custom.min.css'
	                )
	        }
	        js = (
	            'javascript/jquery.js',
	            'javascript/jquery-ui-1.8.22.custom.min.js',
	            'javascript/imageselect.js',
	            "javascript/admin.js",)

admin.site.register(Flavor,FlavorAdmin)

admin.site.register(UserSearchTab,SearchTabAdmin)