from django.contrib import admin 
from apps.accounts.models import UserProfile, AnonymousProfile, Question, QuestionAnswer,\
            WaitingList, Answer, BillingInfo, ShippingInfo, CCToken

from django.contrib.flatpages.models import FlatPage
 
# Note: we are renaming the original Admin and Form as we import them
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
 
from django import forms
from ckeditor.widgets import CKEditorWidget
 
class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FlatPage # this is not automatically inherited from FlatpageFormOld
 
 
class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm
 


class WaitingListAdmin(admin.ModelAdmin):
    list_display  = ('email', 'added', 'approved')
    list_filter   = ('approved',)
    search_fields = ('email',)


admin.site.register(WaitingList, WaitingListAdmin)
 
# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.register(UserProfile)
admin.site.register(AnonymousProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionAnswer)
admin.site.register(BillingInfo)
admin.site.register(ShippingInfo)
admin.site.register(CCToken)