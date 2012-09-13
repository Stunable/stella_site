from django.contrib import admin 
from contact_form.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('created', 'firstname', 'lastname', 'email')

admin.site.register(Contact, ContactAdmin)
