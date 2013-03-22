from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.datetime_safe import datetime
from django.utils.hashcompat import sha_constructor
from random import random
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from tagging.models import Tag
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.contrib.localflavor.us.models import PhoneNumberField

from apps.common.forms import FedexTestAddress

from django.forms.models import model_to_dict


AGE_RANGE_CHOICE = (
    ('','optional'),
    ('20 or younger','20 or younger'),
    ('20-30','20-30'),
    ('30-40','30-40'),
    ('40-50','40-50'),
    ('50-60','50-60'),
    ('60 or older','60 or older'),
)

class ProfileBase(object):

    def update_product_group_tag(self, product_group):
        tags = [tag.name for tag in Tag.objects.get_for_object(self) if not tag.name.startswith('product_group_')]
        if product_group:
            tags.append(product_group)
        Tag.objects.update_tags(self, ','.join(tags))

    def set_default_tags(self):
        tags = [tag.name for tag in Tag.objects.filter(is_default=True)]
        Tag.objects.update_tags(self.user, ','.join(tags))


class UserProfile(models.Model,ProfileBase):
    """
    User profile model
    """

    user = models.ForeignKey(User, unique=True)
    avatar = models.ImageField(upload_to='upload', null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    age_range = models.CharField(max_length=30,choices=AGE_RANGE_CHOICE, default='optional')
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    favourite_designer = models.CharField(max_length=100, null=True, blank=True)
    view_happenings = models.BooleanField(default=True)
    
    default_cc = models.CharField(max_length=6, null=True, blank=True, editable=False)
    first_login = models.BooleanField(default=True)
    
    def __unicode__(self):
        try:
            return "%s's profile" % self.user
        except:
            return "Somebody's user profile"
    
    @property
    def avatar_image(self):
        """Gets profile picture as a thumbnail and returns the url or returns the default image"""
        if self.avatar:
            return self.avatar.url
        return "/static/images/default_avatar.gif"
        
    @property
    def location(self):
        return "San Francisco, CA"
        


class AnonymousProfile(models.Model,ProfileBase):
    favourite_designer = models.CharField(max_length=100, null=True, blank=True)
    first_login = models.BooleanField(default=True)


def user_new_unicode(self):
    return "Stella's Favorite" if self.get_full_name() == "" else self.get_full_name()
# Replace the __unicode__ method in the User class with out new implementation
User.__unicode__ = user_new_unicode 
    
class Question(models.Model):
    question = models.CharField(max_length=256)
    active = models.BooleanField()
    
    def __unicode__(self):
        return self.question
    
class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=256)

    def __unicode__(self):
        return self.question.question + ' ' + self.answer
    
class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    profile = models.ForeignKey(UserProfile)

WAITLIST_SHOPPER_SUBJECT = "accounts/waitlist_shopper_subject.txt"
WAITLIST_SHOPPER_MESSAGE = "accounts/waitlist_shopper_message.txt"
WAITLIST_ADMIN_FYI_SUBJECT = "accounts/waitlist_admin_fyi_subject.txt"
WAITLIST_ADMIN_FYI_MESSAGE = "accounts/waitlist_admin_fyi_message.txt"

class WaitingListManager(models.Manager):
    
    def send_invitation_notice(self, to_email):
        # send notification email to requester and admin
            salt = sha_constructor(str(random())).hexdigest()[:5]
            confirmation_key = sha_constructor(salt + to_email).hexdigest()
            
            user_ctx = {'email': to_email}
            
            # send notification email to requester
            waitlist_user_subject = render_to_string(WAITLIST_SHOPPER_SUBJECT, user_ctx)
            waitlist_user_message = render_to_string(WAITLIST_SHOPPER_MESSAGE, user_ctx)
            send_mail(waitlist_user_subject, waitlist_user_message, settings.STELLA_DEFAULT_EMAIL, [to_email])
            
            admin_url = u"http://%s/admin/" % (
                    unicode(Site.objects.get_current())
                )
            
            admin_ctx = {'admin_url': admin_url}
            # send notifications email to admin
            admin_subject = render_to_string(WAITLIST_ADMIN_FYI_SUBJECT, admin_ctx)
            admin_message = render_to_string(WAITLIST_ADMIN_FYI_MESSAGE, admin_ctx)
            send_mail(admin_subject, admin_message, settings.STELLA_DEFAULT_EMAIL, [mail_tuple[1] for mail_tuple in settings.CONTACT_LIST])
            
            new_user = WaitingList(email=to_email, confirmation_key=confirmation_key)
            new_user.save()
    
    def send_invitation(self, to_email, message, subject, email_message, confirmation_key):
        try:
#            salt = sha_constructor(str(random())).hexdigest()[:5]
#            confirmation_key = sha_constructor(salt + to_email).hexdigest()
            
            accept_url = u"http://%s%s" % (
                unicode(Site.objects.get_current()),
                reverse("new_user_join", args=(confirmation_key,)),
            )
            
            ctx = {
                "email": to_email,
                "SITE_NAME": settings.SITE_NAME,
                "CONTACT_EMAIL": settings.CONTACT_EMAIL,
                "message": message,
                "accept_url": accept_url,
            }
            subject = render_to_string(subject, ctx)
            email_message = render_to_string(email_message, ctx)
#            new_user = WaitingList(email=to_email, confirmation_key=confirmation_key)
#            new_user.save()
#            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [to_email])
            send_mail(subject, email_message, settings.STELLA_DEFAULT_EMAIL, [to_email])
        except:
            pass
        
WAITLIST_MSG = "You have request an invite from stella"
SUBJECT = "accounts/waitlist_invite_subject.txt"
EMAIL_MESSAGE = "accounts/waitlist_invite_message.txt"
   
class WaitingList(models.Model):
    email = models.EmailField()
    added = models.DateTimeField(default=datetime.today())
    confirmation_key = models.CharField(max_length=40)
    
    approved = models.BooleanField(default=False)
    
    objects = WaitingListManager()
    
    def __unicode__(self):
        return self.email
    
    def save(self):
        if self.id:
            old_obj = WaitingList.objects.get(pk=self.id)
            if not old_obj.approved and self.approved:
                WaitingList.objects.send_invitation(self.email, WAITLIST_MSG, SUBJECT, EMAIL_MESSAGE, self.confirmation_key)
        super(WaitingList, self).save()

class Address(models.Model):
    """An address which can be used as shipping and/or invoice address.
    """
    customer = models.ForeignKey(UserProfile, verbose_name=_(u"Customer"), blank=True, null=True, related_name="addresses")

    firstname = models.CharField(_("First Name"), max_length=50)
    lastname = models.CharField(_("Last Name"), max_length=50)
    company_name = models.CharField(_("Company Name"), max_length=50, blank=True, null=True)
    address1 = models.CharField(_("Address 1"), max_length=100)
    address2 = models.CharField(_("Address 2"), max_length=100, blank=True, null=True)
    city = models.CharField(_("City"), max_length=50)
    state = models.CharField(_("State"), max_length=50, choices=STATE_CHOICES)
    zip_code = models.CharField(_("Zip code"), max_length=10)
    country = models.CharField(_("Country"), default='US', choices=(('US', 'United States'), ), max_length=250,)
    phone = PhoneNumberField(_("Phone"))
    email = models.EmailField(_("E-Mail"), blank=True, null=True, max_length=50)

    @staticmethod
    def verify_address(data=None):
        print 'VERIFY ADDRESS ON SHIPPING FORM'
        F = FedexTestAddress(data)
        return F.validate().processed()



    def __unicode__(self):
        return "%s / %s / %s" % (self.address1, self.city, self.state)
    
class ShippingInfo(Address):
    is_default = models.BooleanField(default=False)
    
class BillingInfo(Address):
    pass

class CCToken(models.Model):
    cc_name = models.CharField(max_length=32)
    user_name = models.CharField(max_length=100)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    token = models.CharField(max_length=250,unique=True)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    is_authorized = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.__unicode__()+'_'+self.cc_name
    
    class Meta:
        unique_together =(('user','cc_name'))
    
    def save(self,*args,**kwargs):
        if self.user:
            if CCToken.objects.filter(user=self.user, is_default=True).count() == 0:
                # there is no default cc then the newly created CC should be the default one
                self.is_default = True
       
        super(CCToken, self).save(self)

    def authorize(self):
        pass


    