from django.contrib import admin
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','is_default','slug')
    list_filter = ('is_default',)
    search_fields = ('name',)
    form = TagAdminForm
    # prepopulated_fields = {"slug": ("name",)}

admin.site.register(TaggedItem)
admin.site.register(Tag, TagAdmin)




