import sha
import re
import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class InvitationManager(models.Manager):
    """
    Provides table-level functionality on the list of emails
    we are going to have for user signups. 

    The methods defined here provide shortcuts to: 
    - creating a new beta-user, defined as a user that has requested an 
      invitation to the site. 
    - 
    
    """
    def register_invite(self, activation_key):
        """
        Validate an activation key which should allow the corresponding user to 
        register if valid.
        Returns whether or not the key is valid. 
        """
        if SHA1_RE.search(activation_key):
            try: 
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                return True
        return False

    def finalize_invite(self, activation_key):
        """
        Upon registration of a user using this particular activation key,
        invalidate the key so that it cannot be used again.
        """
        try:
            profile = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False
        return profile.destroy_key()

    def create_invite_profile(self, email):
        """
        Creates and returns a new BetaInviteProfile with
        necessary activation key logic. 
        """
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+email).hexdigest()
        profile = self.create(email=email,
                              activation_key=activation_key)

        # Send the thank you email
        profile.thank_you_email()
        return profile
                           
    def invite_specific_regex(self, regex):
        """
        Emails all email addresses with a matching regex. Can
        be used to email a specific domain eg. @google.com, or 
        for emailing a specific person directly if their email is known.
        """
        pass

    def invite_specific_age(self, time_days):
        """
        Emails all persons who have signed up for the beta at least
        time_days days ago. Useful for bringing in users based on how 
        early they signed up.
        """
        pass

    def invite_all(self):
        """
        Invites all the remaining people who have not yet been emailed.
        Useful for closing out the beta and allowing everyone to join. 
        """
        pass


class BetaInviteProfile(models.Model):
    """
    A simple profile which stores an activation key for use during user
    account registration. Also stores relevant metadata with invitation request.
    """

    ACTIVATED = u"ALREADY_ACTIVATED"

    activation_key = models.CharField(_('activation key'), max_length=40)
    date_created = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=75)
    invited = models.BooleanField(default=False)

    objects = InvitationManager()

    class Meta:
        verbose_name = _('invitation profile')
        verbose_name_plural = _('invitation profiles')

    def __unicode__(self):
        return u"Invitation request from %s" % self.email_address

    def activation_key_expired(self):
        """
        An activation key is expired only after it is used by the user, and 
        will be reset to the string "ALREADY_ACTIVATED". Re-activating is not 
        permitted, and so this method returns true in this case. 
        """
        return self.activation_key == self.ACTIVATED

    def destroy_key(self):
        """
        Renders the stored activation key void by reseting it to the 
        string "ALREADY_ACTIVATED".
        """
        self.activation_key = self.ACTIVATED
        self.save()
        return True

    def thank_you_email(self):
        """
        Sends an email to this profile thanking them for signing up.
        """
        current_site = Site.objects.get_current()
        subject = render_to_string('beta_invite/thank_you_email_subject.txt',
                                   {'site': current_site})
        subject = ''.join(subject.splitlines())
        message = render_to_string('beta_invite/thank_you_email.txt',
                                   {'site':current_site})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, self.email)

    def invite(self):
        """
        Sends an email to this profile with a link that will allow them to 
        register for an account. 
        """
        current_site = Site.objects.get_current()
        subject = render_to_string('beta_invite/invitation_email_subject.txt',
                                   { 'site': current_site })
        # Email subject must not contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('beta_invite/invitation_email.txt',
                                   { 'activation_key': self.activation_key,
                                     'site': current_site})
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, self.email)
        self.invited = True
