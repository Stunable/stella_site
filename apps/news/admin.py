from django.contrib import admin
from django import forms
from apps.news.models import *
from apps.ckeditor.widgets import CKEditorWidget
 

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)

class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    tease = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post

class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status')
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    
    form = PostAdminForm
admin.site.register(Post, PostAdmin)


class Ext_News_Admin(admin.ModelAdmin):
    list_display = ('source','post_type','date')

    actions = ('refresh_content',)


    def refresh_content(self,request,queryset):
        for obj in queryset:
            obj.refresh_content()

admin.site.register(ExternalPost,Ext_News_Admin)