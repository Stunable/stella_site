from django.forms import ModelForm
from contact_form.models import Contact
from common.forms import AjaxModelForm

class ContactForm(AjaxModelForm):
    
    class Meta:
        model = Contact