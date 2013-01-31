from django import forms
from django.contrib.auth.models import User
from accounts.models import WaitingList
from django.forms.widgets import CheckboxSelectMultiple  

from django.conf import settings
from apps.racks.models import Color, Size
from apps.racks.forms import addPlus
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

try:
    from apps.bootstrap.forms import BootstrapForm as SUIStyleForm, BootstrapModelForm as SUIStyleModelForm, Fieldset
except:
    from django.forms import Form as SUIStyleForm

from django.contrib.localflavor.us.us_states import US_STATES
from retailers.models import RetailerProfile, StylistItem, ShippingType
from racks.models import Item, Rack, Rack_Item,ProductImage

from tagging.models import Tag

attrs_dict = {}      
from apps.common.forms import testAddress
from apps.cart.plugins.taxcloud import TaxCloudClient
TCC = TaxCloudClient()

WAITLIST_MSG = "You have request an invite from stella"
SUBJECT = "accounts/waitlist_invite_subject.txt"
EMAIL_MESSAGE = "accounts/waitlist_invite_message.txt"
RETAILER_SUBJECT = 'accounts/retailer_welcome_subject.txt'
RETAILER_MESSAGE = 'accounts/retailer_welcome_message.txt'
            
SELLING_OPTIONS = (
    ('no no', 'I do not have a website, and I do not sell my products online'),
    ('no yes', 'I do not have a website, but I do sell my products online'),
    ('yes no', 'I have a website, but do not sell my products online'),
    ('yes yes', 'I have a website and I sell my products on it')
)

class RetailerEditForm(forms.ModelForm):
    email_address = forms.EmailField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    shipping_type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=ShippingType.objects.all(), required=False)
    
    class Meta:
        model = RetailerProfile
    
        fields = ('email_address', 'city', 'state','password', 'description')
    
    def clean_shipping_type(self):
        if self.cleaned_data.get('shipping_type') and len(self.cleaned_data.get('shipping_type')) > 0:
            return self.cleaned_data.get('shipping_type')
        else:
            return self.instance.shipping_type.all()
    
    def clean_address_1(self):
        if self.cleaned_data.get('address_1') and len(self.cleaned_data.get('address_1')) > 0:
            return self.cleaned_data.get('address_1')
        else:
            return self.instance.address_1
    
    def clean_address_2(self):
        if self.cleaned_data.get('address_2') and len(self.cleaned_data.get('address_2')) > 0:
            return self.cleaned_data.get('address_2')
        else:
            return self.instance.address_2
    
    def clean_description(self):
        if self.cleaned_data.get('description') and len(self.cleaned_data.get('description')) > 0:
            return self.cleaned_data.get('description')
        else:
            return self.instance.description
    
    def clean_city(self):
        if self.cleaned_data.get('city') and len(self.cleaned_data.get('city')) > 0:
            return self.cleaned_data.get('city')
        else:
            return self.instance.city
            
    def clean_state(self):
        if self.cleaned_data.get('state') and len(self.cleaned_data.get('state')) > 0:
            return self.cleaned_data.get('state')
        else:
            return self.instance.state
    
   
    
    def clean_email_address(self):
        if self.cleaned_data.get('email_address'):
            if self.cleaned_data.get('email_address') != self.instance.email_address:
                users = User.objects.filter(email=self.cleaned_data.get('email_address'))
                if users.count() > 0:
                    raise forms.ValidationError("Email has already been used!")
            return self.cleaned_data.get('email_address')
        else:
            return self.instance.email_address





class RetailerProfileCreationForm(forms.ModelForm):
    first_name = forms.CharField(required=False, error_messages={'required': (u'Stella wants to know your first name')})
    last_name = forms.CharField(required=False, error_messages={'required': (u'Stella wants to know your last name')})
    state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'required', 'id': 'state'}), choices=US_STATES,error_messages={'required': (u'State is required')} )
    description = forms.CharField(widget=forms.Textarea(attrs=dict(cols=50, rows=5, placeholder=(u"Tell us a little something about\
                                 yourself and the products you sell. Hit us with your best elevator pitch in under 600 words!"))),
                                  max_length=600, help_text='600 characters max.', required=True, error_messages={'max_length': (u'Your description must be less than 600 words')})
    password = forms.CharField(widget=forms.PasswordInput(), required=True, error_messages={'required': (u'Password is required')})
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True, error_messages={'required': (u'Password Confirm is required')})
    selling_options = forms.MultipleChoiceField(required=False,choices=SELLING_OPTIONS, widget=forms.CheckboxSelectMultiple, error_messages={'required': (u'Selling options is required')})
    more_details = forms.CharField(required=False)
#    terms = forms.BooleanField(error_messages={'required': (u'You must agree to the terms and conditions')})
    
    class Meta:
        model = RetailerProfile
    
    def clean_email_address(self):
        email_address = self.cleaned_data['email_address']
        retailers = RetailerProfile.objects.filter(email_address = email_address) 
        users = User.objects.filter(email=email_address)
        waiting_list = WaitingList.objects.filter(email=email_address)
        
        if retailers.count() > 0 or users.count() > 0 or waiting_list.count() > 0:
            raise forms.ValidationError(u"This email had already been registered")
        else:
            return self.cleaned_data['email_address']
    
    def clean_more_details(self):
        return
        if 'selling_options' in self.cleaned_data:
            if self.cleaned_data['selling_options'] == 'no yes' and not self.cleaned_data['more_details']:
                raise forms.ValidationError("Please enter your web address!")
            elif self.cleaned_data['selling_options'] == 'yes no' and not self.cleaned_data['more_details']:
                raise forms.ValidationError("Where to you currently sell online?")
            elif self.cleaned_data['selling_options'] == 'yes yes' and not self.cleaned_data['more_details']:
                raise forms.ValidationError("Please enter your web address!")
            
    # def clean_not_accept_refund(self):
    #     if not self.cleaned_data.get('accept_refund') and not self.cleaned_data['not_accept_refund'] :
    #         raise forms.ValidationError("Please Accept or not Accept Refund Policy")
    #     return self.cleaned_data['not_accept_refund'] 
    
    def clean_accept_refund(self):
        if not self.cleaned_data['accept_refund']:
            raise forms.ValidationError('you must accept the terms')
        return self.cleaned_data['accept_refund'] 
    
    def clean_selling_options(self):
        try:
            return self.cleaned_data['selling_options'][0]
        except:
            return ''
    
    def clean_password(self):
        return self.cleaned_data['password']
        
    def clean_password_confirm(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirm']
        if password1 != password2:
            raise forms.ValidationError("Your password doesn't match")
        return self.cleaned_data['password_confirm']
    
    def clean(self):
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError("Your password doesn't match")

        T = testAddress(self.cleaned_data)
        V = TCC.verify_address(testAddress(self.cleaned_data))

        if V.ErrNumber != "0":
            if 'City' in V.ErrDescription:
                # self._errors['city'] = self._errors.get('city', [])
                self._errors['city']= self.error_class([V.ErrDescription])
            elif 'Zip Code' in V.ErrDescription:
                self._errors['zip_code']= self.error_class([V.ErrDescription])
            else:
                raise forms.ValidationError(V.ErrDescription)
        else:
            for user,test in T.fieldmap:
                if hasattr(T,user) and hasattr(V,test):
                    if getattr(T,user).upper() == getattr(V,test).upper():
                        print getattr(T,user)
                    else:
                        print getattr(T,user),':',getattr(V,test)

        return self.cleaned_data
    
    def save(self, force_insert=False, force_update=False, commit=True):
        if self.cleaned_data.get('email_address'):
            email_address = self.cleaned_data.get('email_address')
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            password = self.cleaned_data.get('password')
            new_user = User(username=email_address, first_name=first_name, last_name=last_name, email=email_address)
            new_user.set_password(password)
            new_user.is_active=False
            new_user.save()
            
        return super(RetailerProfileCreationForm, self).save()
    

from common.forms import AjaxModelForm


class ItemForm(AjaxModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    
    class Meta:
        model = Item
        exclude = ('fabrics', 'image_urls', 'order', 'retailers', 'tags', 'sizes', 'colors','upload','price','is_onsale','is_available', 'approved','is_deleted','bg_color','api_type','object_id','slug','_retailer','price_text')
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ItemForm, self).__init__(*args, **(kwargs))
        self.fields['tags'].label = "Tags Related to your Product"
        self.fields['featured_image'].empty_label = '/static/images/choosepic.png'
        self.fields['featured_image'].queryset = ProductImage.objects.filter(retailer=user)
        addPlus(self.fields['featured_image'].widget, 'featured_image', None, ProductImage.objects.filter(retailer=user),'#','Product Image')



    def clean_colors(self):
        return None
        
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        try:
            float(price)
        except:
            raise forms.ValidationError("Price must be a number!")
        return self.cleaned_data.get('price')
    
    def clean_inventory(self):
        inventory = self.cleaned_data.get('inventory')
        try:
            float(inventory)
        except:
            raise forms.ValidationError("Inventory must be a number!")
        return self.cleaned_data.get('inventory')
    
    def save(self, force_insert=False, force_update=False, commit=True):
        self.item = super(ItemForm, self).save(commit=commit)
        if commit:
            self.finish_save()
        return self.item

    def finish_save(self):
        self.item.save()
        si = StylistItem.objects.get_or_create(stylist=self.user, item=self.item)
        # add item to default racks
        try:
            rack = Rack.objects.get(name=self.item.category)
            rack_item = Rack_Item.objects.get_or_create(user=self.user, rack=rack, item=self.item)
        except:
            # log bug here
            pass

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('colors', 'fabrics', 'image_urls', 'order', 'upload', 'is_available', 'price', 'approved','api_type','object_id','slug','_retailer','price_text')
    
    def __init__(self, *args, **kwargs):
        super(ItemEditForm, self).__init__(*args, **(kwargs))
        self.fields['featured_image'].required = False
        self.fields['featured_image'].empty_label = '/static/images/choosepic.png'
        self.fields['featured_image'].queryset = ProductImage.objects.filter(retailer=user)
        addPlus(self.fields['featured_image'].widget, 'featured_image', None, ProductImage.objects.filter(retailer=retailer),'#','Product Image')

    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        try:
            float(price)
        except:
            raise forms.ValidationError("Price must be a number!")
        return self.cleaned_data.get('price')
    
    def clean_inventory(self):
        inventory = self.cleaned_data.get('inventory')
        try:
            float(inventory)
        except:
            raise forms.ValidationError("Inventory must be a number!")
        return self.cleaned_data.get('inventory')
    
    def save(self, force_insert=False, force_update=False, commit=True):
        category_update = False
        try:
            old_item = Item.objects.get(pk=self.instance.id)
            if self.cleaned_data.get('category').name != old_item.category.name:
                category_update = True
                #remove old rack_item relationship
                old_rack = Rack.objects.get(name=old_item.category)
                old_rack_item = Rack_Item.objects.get(rack=old_rack, item=old_item)
                old_rack_item.delete()
            item = super(ItemEditForm, self).save(commit=commit)
            
            if category_update:
                new_rack = Rack.objects.get(name=item.category)
                rack_item = Rack_Item(rack=new_rack, item=item)
                rack_item.save()
        except:
            # log bug here
            pass
        
        return item

class LogoUploadForm(forms.ModelForm):
    class Meta:
        model=RetailerProfile
        fields = ('company_logo',)
