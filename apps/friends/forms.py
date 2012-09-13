from django import forms
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from notification.models import Notice


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


from django.contrib.auth.models import User
from apps.friends.models import FriendshipInvitation, JoinInvitation


class MultiEmailField(forms.Field):
    '''
    class MultiEmailField enable multi emails that are seperated by commas
    '''
    
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return [e.strip() for e in value.split(',')]

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email.strip())

EMAILS_MSG = "Enter email addresses here, seperated by commas"
EMAIL_MESSAGE_MSG = "Write your message here..."
SUBJECT = "friends/join_invite_subject.txt"
EMAIL_MESSAGE = "friends/join_invite_message.txt"

FRIEND_INVITE_SUBJECT = "friends/friend_invite_subject.txt"
FRIEND_INVITE_MESSAGE = "friends/friend_invite_message.txt"


class InviteFriendForm(forms.Form):
    
    emails = MultiEmailField(required=True, widget=forms.TextInput(attrs={'placeholder':EMAILS_MSG, 'class':'txt'}))
    email_message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':EMAIL_MESSAGE_MSG}))
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        self.non_user_emails = set()
        super(InviteFriendForm, self).__init__(*args, **kwargs)
        
    def clean_emails(self):
        emails = self.cleaned_data["emails"]
        if not emails:
            raise forms.ValidationError("Please enter valid emails that are seperated by a comma")
            
        return self.cleaned_data["emails"]
    
    def clean(self):
        emails = set(self.cleaned_data.get("emails", []))
        if not emails:
            raise forms.ValidationError("Please enter valid emails that are seperated by a comma")
        
        #emails = set([e.strip() for e in self.cleaned_data["emails"].split(',')])
         
        # check this user and others people are friend of each other or not
        for to_user in User.objects.filter(email__in=emails):
            emails.remove(to_user.email)
            previous_invitations_to = FriendshipInvitation.objects.invitations(to_user=to_user, from_user=self.user)
            if previous_invitations_to.count() > 0:
                raise forms.ValidationError(u"Already requested friendship with %s" % to_user.username)
            
            # check inverse            
            previous_invitations_from = FriendshipInvitation.objects.invitations(to_user=self.user, from_user=to_user)
            if previous_invitations_from.count() > 0:
                raise forms.ValidationError(u"%s has already requested friendship with you" % to_user.username)        
         
        self.non_user_emails = emails
        return self.cleaned_data
    
    def save(self):
        # those users have not registered yet
        for email in self.non_user_emails:
#            join_request = JoinInvitation.objects.send_invitation(self.user, email, self.cleaned_data["email_message"], SUBJECT, EMAIL_MESSAGE)
            join_request = JoinInvitation.objects.send_invitation(self.user, email, self.cleaned_data["email_message"], FRIEND_INVITE_SUBJECT, FRIEND_INVITE_MESSAGE)
            self.user.message_set.create(message="Invitation to join sent to %s" % join_request.contact.email)
        
        emails = self.cleaned_data["emails"]
        invitations = []
        email_ctx = {'sender': self.user}
        for to_user in User.objects.filter(email__in=emails):
            
            message = self.cleaned_data["email_message"]
            invitation = FriendshipInvitation(from_user=self.user, to_user=to_user, message=message, status="2")
            invitation.save()
            if notification:
                notification.send([to_user], "friends_invite", {"invitation": invitation, 'sender': self.user}, True, self.user)
                
                # get the latest notification
                notices = Notice.objects.filter(recipient=to_user, sender=self.user, notice_type=3).order_by('-added')
                if notices:
                    notice = notices[0]
                    accept_url = u"http://%s%s" % (
                        unicode(Site.objects.get_current()),
                        unicode(reverse("accept_invitation", args=[self.user.id, notice.id]))
                    )
                    # send email
                    email_ctx['recipient'] = to_user
                    email_ctx['approval_link'] = accept_url
                    
                    notification.send_notification_on("friend-invite-sent", sender=self.user, recipient=to_user, approval_link=accept_url)
#                    subject = render_to_string(FRIEND_INVITE_SUBJECT, email_ctx)
#                    email_message = render_to_string(FRIEND_INVITE_MESSAGE, email_ctx)
#                    send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [to_user.email])
            
            self.user.message_set.create(message="Friendship requested with %s" % to_user.username) # @@@ make link like notification
            invitations.append(invitation)
        return invitations



