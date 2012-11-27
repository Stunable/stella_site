from django import forms
from apps.accounts.models import AGE_RANGE_CHOICE
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import validators
from accounts.models import UserProfile, WaitingList

from django.conf import settings
from accounts.models import BillingInfo, ShippingInfo
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.template.context import Context
from racks.models import Brand
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
    

from apps.common.forms import testAddress
from apps.cart.plugins.taxcloud import TaxCloudClient
TCC = TaxCloudClient()

from django.core.mail import send_mail
from django.contrib.localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _
from apps.common.forms import AjaxForm
attrs_dict = {}

class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    view_happenings = forms.BooleanField(label="Would you like to see Happenings?", required=False)
    
    class Meta:
        model = UserProfile
        exclude = ('favourite_designer', 'age_range', 'zipcode', 'avatar', 'user', 'first_login')
    
    def clean_view_happenings(self):
        if self.cleaned_data.get('view_happenings'):
            return True
        else:
            return False
    
    def clean_email(self):
        if self.cleaned_data.get('email'):
            if self.cleaned_data.get('email') != self.instance.user.email:
                users = User.objects.filter(email=self.cleaned_data.get('email'))
                if users.count() > 0:
                    raise forms.ValidationError("Email has already been used!")
            return self.cleaned_data.get('email')
        else:
            return self.instance.user.email

class AccountSettingsForm(AjaxForm):
    firstname = forms.CharField(required = True, label="First Name", error_messages={'required': 'Stella wants to know you on a first name basis.'})
    lastname = forms.CharField(required = False, label="Last Name", error_messages={'required': 'Stella wants to know you on a last name basis.'})

    zipcode = forms.CharField(widget=forms.TextInput(attrs=dict(placeholder="Optional")),required=False)
    age_range = forms.ChoiceField(widget=forms.Select(), choices=AGE_RANGE_CHOICE, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label="Password",
                                required=True)

    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label="Re-type Password",
                                required=True)
    view_happenings = forms.BooleanField(label="Would you like to see Happenings?", required=False)
    
    avatar = forms.ImageField(required = False, error_messages={'invalid_image': 'Please upload a valid image file!'})

    def clean_view_happenings(self):
        if self.cleaned_data.get('view_happenings'):
            return True
        else:
            return False
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Your password doesn't match")
        
        if 'email' in self.cleaned_data and 'email_again' in self.cleaned_data:
            if self.cleaned_data['email'] != self.cleaned_data['email_again']:
                raise forms.ValidationError("Your email address doesn't match")
                        
        return self.cleaned_data
    
class AccountCreationForm(forms.Form):
    firstname = forms.CharField(required = True, label="First Name")
    lastname = forms.CharField(required = True, label="Last Name")
    
    email = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=60)),
                             label="Email", required = True,
                             validators=[validators.validate_email],
                             error_messages={'invalid': (u'Stella can\'t reach you there')})
    email_again = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=60)),
                             label="Re-type email",
                             required=True,
                             validators=[validators.validate_email],
                             error_messages={'invalid': (u'Stella can\'t reach you there')})
    # TODO: add validator for zipcode, add max_length check too
    zipcode = forms.CharField(required=False)
    age_range = forms.ChoiceField(widget=forms.Select(attrs={'class': 'styled inline optional', 'tabindex': '6'}), choices=AGE_RANGE_CHOICE, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label="Password", max_length = 12, min_length = 6,
                                required=True)

    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label="Re-type Password", max_length = 12, min_length = 6,
                                required=True)
        
    def clean_email(self):        
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(u"User already exits")
    
    def clean_email_again(self):
        email_again = self.cleaned_data.get('email_again')
        email = self.cleaned_data.get('email')
        if email:
            if email_again != email:
                raise forms.ValidationError("Your email address doesn't match")
        
        return self.cleaned_data['email_again']
    
    def clean_password1(self):
        return self.cleaned_data['password1']
        
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Your password doesn't match")
        return self.cleaned_data['password2']
            

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Your password doesn't match")
        
        if 'email' in self.cleaned_data and 'email_again' in self.cleaned_data and self.cleaned_data.get('email_again'):
            if self.cleaned_data['email'] != self.cleaned_data['email_again']:
                raise forms.ValidationError("Your email address doesn't match")

        return self.cleaned_data
    

class AvatarUploadForm(forms.ModelForm):
    
    class Meta:
        model=UserProfile
        fields = ('avatar',)
        
class FavouriteDesignerForm(forms.ModelForm):
    
    favourite_designer = forms.ModelChoiceField(queryset=Brand.objects.all(), 
                                                widget=forms.Select(attrs={'class': 'txt inline', "style": "width: 300px"}),
                                                error_messages={'required': (u'Please select your favourite brand of Jeans!')})
    
    class Meta:
        model = UserProfile
        fields = ('favourite_designer',)
        
        

#WAITLIST_MSG = "You have request an invite from stella"
#SUBJECT = "accounts/waitlist_invite_subject.txt"
#EMAIL_MESSAGE = "accounts/waitlist_invite_message.txt"

 
class WaitlistForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             error_messages={'invalid': (u'Stella can\'t reach you there')})
#    def __init__(self, *args, **kwargs):
#        self.user = User.objects.get(username="admin")
#        super(WaitlistForm, self).__init__(*args, **kwargs)
        
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(u'This email address is already in use.')
        return self.cleaned_data['email']
    
    def save(self):
        # those users have not registered yet
        email = self.cleaned_data['email']
        if email:
            WaitingList.objects.send_invitation_notice(email)
#            join_request = WaitingList.objects.send_invitation(email, WAITLIST_MSG, SUBJECT, EMAIL_MESSAGE)
            
            
from common.forms import AjaxModelForm

class BillingInfoForm(AjaxModelForm):
    customer = forms.ModelChoiceField(queryset=UserProfile.objects.all(),
            widget=forms.HiddenInput())

    class Meta:
        model = BillingInfo 
        
class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo        
        exclude = ('email', 'company_name', 'is_default', 'customer')

    def clean(self):
        T = testAddress(self.cleaned_data)
        V = TCC.verify_address(testAddress(self.cleaned_data))
        print V
        if V.ErrNumber != "0":
            if 'City' in V.ErrDescription:
                # self._errors['city'] = self._errors.get('city', [])
                self._errors['city']= self.error_class([V.ErrDescription])
            elif 'Address Not Found.' in V.ErrDescription:
                pass
                #self._errors['city']= self.error_class("We could not verify this as an existing address.")
            elif 'Zip Code' in V.ErrDescription:
                self._errors['zip_code']= self.error_class([V.ErrDescription])
            else:
                raise forms.ValidationError(V.ErrDescription)
        else:
            for user,test in T.fieldmap:
                if hasattr(T,user) and hasattr(V,test):
                    #if getattr(T,user).upper() == getattr(V,test).upper():
                    self.cleaned_data[user] = getattr(V,test)
                    #else:
                     #   self.cleaned_data[user] = getattr(V,test)
        return self.cleaned_data

        
class ShippingInfoEditForm(AjaxModelForm):
    class Meta:
        model = ShippingInfo
        exclude = ('is_default', 'compnay_name', 'customer', 'country', 'email')

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password) or authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct email and password. Note that password is case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                "Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in.")

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
