from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import PhoneNumberField
from racks.models import Item

RETAILER_SUBJECT = 'accounts/retailer_welcome_subject.txt'
RETAILER_MESSAGE = 'accounts/retailer_welcome_message.txt'
    
class ShippingType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class RetailerProfile(models.Model):
    """
    Company profile model
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, choices=US_STATES)
    zip_code = models.CharField(max_length=10)
    hours = models.CharField(max_length=50, blank=True)
    phone_number = PhoneNumberField()
    email_address = models.EmailField()
    company_logo = models.ImageField(upload_to='upload')
    description = models.TextField()
    selling_options = models.CharField(max_length=100)
    more_details = models.CharField(max_length=100, blank=True, null=True)
    paypal_email = models.EmailField(null=True)
    shipping_type = models.ManyToManyField(ShippingType, null=True, blank=True)
    accept_refund = models.BooleanField(default=False)
    not_accept_refund = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
#    terms = models.BooleanField(default=False, null=True, blank=True)
    
    def __unicode__(self):
        return self.name.title()
    
    @property
    def logo_image(self):
        """Gets profile picture as a thumbnail and returns the url or returns the default image"""
        return self.company_logo or "upload/default_avatar.gif"
        
    def save(self):
        if self.id:
            old_obj = RetailerProfile.objects.get(pk=self.id)
            if not old_obj.approved and self.approved:
                accept_url = u"http://%s%s" % (
                    unicode(Site.objects.get_current()),
                    reverse("auth_login"),
                )
                ctx = {
                    "accept_url": accept_url,
                    "retailer": self 
                }
                subject = render_to_string(RETAILER_SUBJECT, ctx)
                email_message = render_to_string(RETAILER_MESSAGE, ctx)
                try:
                    new_user = User.objects.get(username=self.email_address)
                    new_user.is_active = True
                    new_user.save()
                    self.user = new_user                    
                except User.DoesNotExist:
                    pass                    
                
#                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [self.email_address])
                send_mail(subject, email_message, settings.STELLA_DEFAULT_EMAIL, [self.email_address])
        super(RetailerProfile, self).save()
        
class StylistItem(models.Model):
    stylist = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    
    def __unicode__(self):
        return self.stylist.username + ' ' + self.item.name