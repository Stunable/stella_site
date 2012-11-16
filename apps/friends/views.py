import json
from django.views.generic.simple import direct_to_template
from apps.friends.forms import InviteFriendForm
from random import random
from apps.racks.models import Rack
from django.utils.hashcompat import sha_constructor
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import simplejson
from django.core.mail import mail_admins, send_mail
from django.utils.translation import ugettext as _
from django.db.models import Q
import sys
from apps.friends.models import Friendship, JoinInvitation, FriendshipInvitation, \
    notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from apps.notification.models import Notice
from accounts.models import UserProfile
from common import get_or_create_profile
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
from retailers.models import RetailerProfile
from notification.models import NoticeType

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def json_view(func):
    def wrap(request, *a, **kw):
        response = None
        try:
            response = func(request, *a, **kw)
            assert isinstance(response, dict)
            if 'result' not in response:
                response['result'] = 'ok'
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Exception, e:
            # Mail the admins with the error
            exc_info = sys.exc_info()
            subject = 'JSON view error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = 'Request repr() unavailable'
                
            import traceback
            message = 'Traceback:\n%s\n\nRequest:\n%s' % (
                '\n'.join(traceback.format_exception(*exc_info)),
                request_repr,
                )
            mail_admins(subject, message, fail_silently=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = _('Internal error') + ': ' + str(e)
            response = {'result': 'error',
                        'text': msg}

        json = simplejson.dumps(response)
        return HttpResponse(json, mimetype='application/json')
    return wrap

@json_view
@login_required
def add(request, user_id):
    result = {'result': True}
    new_friend = get_object_or_404(User, pk=user_id)
    try:
        previous_invitations_to = FriendshipInvitation.objects.invitations(to_user=new_friend, from_user=request.user)
        if previous_invitations_to.count() > 0:
            result['result'] = False
            result['error'] = u"Already requested friendship with %s" % new_friend.username
            return result
        
        # check inverse            
        previous_invitations_from = FriendshipInvitation.objects.invitations(to_user=request.user, from_user=new_friend)
        if previous_invitations_from.count() > 0:
            result['result'] = False
            result['error'] = u"%s has already requested friendship with you" % new_friend.username
            return result
        
        # if user hasn't sent friend request yet
        invitation = FriendshipInvitation(from_user=request.user, to_user=new_friend, status="2")
        invitation.save()
        if notification:
            notification.send([new_friend], "friends_invite", {"invitation": invitation, 'sender': request.user}, True, request.user)
            
            # get the latest notification
            notices = Notice.objects.filter(recipient=new_friend, sender=request.user, notice_type=3).order_by('-added')
            if notices:
                notice = notices[0]
                accept_url = u"http://%s%s" % (
                    unicode(Site.objects.get_current()),
                    unicode(reverse("accept_invitation", args=[request.user.id, notice.id]))
                )                    
                notification.send_notification_on("friend-invite-sent", sender=request.user, recipient=new_friend, approval_link=accept_url)
        
    except:
        #TODO: log error here
        result['result'] = False
        result['error'] = "Something happened! Please try again!"
        
    return result

@login_required
def fb_add(request, fb_id):
    return add(request,fb_id)

@login_required
def invite(request, template="friends/invite_friends.html"):
    ctx = {}
    if request.method == 'POST':
        ctx['success'] = False
        
        form = InviteFriendForm(request.user, request.POST)
        if form.is_valid():            
            try:
                form.save()
                ctx['success'] = True
                response_data = {'result': 'ok'}
                return HttpResponse(json.dumps(response_data), mimetype="application/json")
            except:
                ctx['message'] = 'Error occurs during sending emails'
        else:
            response_data = {'result': 'error', 'errors': form.errors  }
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
#            ctx['errors'] = form.errors
        ctx['form'] = form
    else:
        form = InviteFriendForm()
        ctx['form'] = form
    
    if request.is_ajax():
        template = "friends/invite_friends_dialog.html"
#        if form.is_valid():
#            return {'result': 'ok'}
#        else:
#            return {'result': 'error', 'errors': form.errors}
    
    return direct_to_template(request, template, ctx)

@login_required
def invite_modal(request, template="friends/invite_friends_dialog.html"):
    ctx = {}
    if request.method == 'POST':
        ctx['success'] = False
        form = InviteFriendForm(request.user, request.POST)
        if form.is_valid():
            ctx['success'] = True
            form.save()
        ctx['form'] = form
    else:
        form = InviteFriendForm()
        ctx['form'] = form
    
    return direct_to_template(request, template, ctx)
  
@login_required
def query_friends(request, q):
    out = []
    if request.session.has_key('friends'):
        out = [f for f in request.session['friends'] if f['name'].lower().startswith(q.lower())]
    #return HttpResponse(json.dumps(out, ensure_ascii=False), mimetype='application/json')
    return out


@login_required
def search(request, template="friends/admirers.html"):
    search_string = request.GET.get('q', '')
    filter_by = request.GET.get('filter', '')
    user_friends = Friendship.objects.friends_for_user(request.user)
    result = []
    user_list = []
    
    if request.is_ajax():
        # ajax request friend search
        if search_string:
            user_list = User.objects.filter(Q(first_name__icontains=search_string)|\
                                         Q(last_name__icontains=search_string)|\
                                         Q(email__icontains=search_string))
        else:
            user_list = User.objects.all()
        
        # remove current user from return queryset
        user_list = user_list.exclude(Q(email=request.user.email)|Q(username=request.user.username))
        friend_list = Friendship.objects.friends_for_user(request.user)
        for friend in friend_list:
            user_list = user_list.exclude(Q(email=friend['friend'].email)|Q(username=friend['friend'].username))
        
        # remove retailer profile from return queryset
        retailers = RetailerProfile.objects.filter(user__isnull=False).values('user')
        user_list = user_list.exclude(pk__in = retailers)
        user_list = user_list[:10]
        
        # add the friend pending list
        pending_from = FriendshipInvitation.objects.filter(Q(status='1')|Q(status='2')).filter(from_user=request.user).values('to_user__pk')
        pending_to = FriendshipInvitation.objects.filter(Q(status='1')|Q(status='2')).filter(to_user=request.user).values('from_user__pk')
        
        pending_from_list = [x['to_user__pk'] for x in pending_from]
        pending_to_list = [x['from_user__pk'] for x in pending_to]
        
#        result_list = list(result)
        template = "friends/partial_user_list.html"
        return direct_to_template(request, template, {'friend_list': query_friends(request,search_string),  'user_list': user_list, 'pending_from_list': pending_from_list, 'pending_to_list': pending_to_list})
    else:
        for fs_u in user_friends:
            if filter_by == "first_name" and search_string in fs_u['friend'].first_name:
                    result.append({'friend': fs_u['friend']})
            if filter_by == "last_name" and search_string in fs_u['friend'].last_name:
                    result.append({'friend': fs_u['friend']})
            if filter_by == "shared_racks" and search_string in Rack.objects.SharedRacksForUser(fs_u['friend']):
                    result.append({'friend': fs_u['friend']})
            if filter_by == "location":
                try:
                    profile = fs_u['friend'].get_profile()
                    if search_string in profile.zipcode:
                        result.append({'friend': fs_u['friend']})
                except UserProfile.DoesNotExist:
                    pass
            if filter_by == "filter_by":
                if search_string in fs_u['friend'].username or\
                    search_string in fs_u['friend'].email or\
                    search_string in fs_u['friend'].first_name or\
                    search_string in fs_u['friend'].last_name:
                    result.append({'friend': fs_u['friend']})
            
        ctx = {'friends_list': result}
    return direct_to_template(request, template, ctx)

@login_required
def index(request, template="friends/admirers.html"):
    user_friends = Friendship.objects.friends_for_user(request.user)                                                                                      
    ctx = {'friends_list': user_friends}    
    return direct_to_template(request, template, ctx)

def accept_join(request, confirmation_key, template="friends/admirers.html"):
    ji = JoinInvitation.objects.get(confirmation_key=confirmation_key)
    try:
        #create new user with random password
        password = sha_constructor(str(random())).hexdigest()[:5]
        user = User(email=ji.contact.email, username=ji.contact.email, first_name='', last_name='')
        user.is_active = True
        user.set_password(password)
        user.save()
            
        ji.accept(user)
        user = authenticate(username=user.email, password=password)
        login(request, user)
        profile = get_or_create_profile(request)
        if request.user.vote_set.all().count() == 0:
            request.session['first_time_login'] = True
        return redirect(reverse("accounts.urls.profile_edit"))
    except:
        # click on invitation link the second time forward
        return redirect(reverse("auth_login"))
    
    return direct_to_template(request, template, {})

ACCEPT_INVITE_SUBJECT = "friends/accept_invite_subject.txt"
ACCEPT_INVITE_MESSGE = "friends/accept_invite_message.txt"

@login_required
def accept_invitation(request, sender_id, notification_id, template="friends/admirers.html"):
    try:
        sender = User.objects.get(pk=sender_id)
        recipient = request.user
        notice = Notice.objects.get(pk=notification_id)
        if notice.recipient != recipient:
            raise Exception("Not Authorized!")
        
        fsi = FriendshipInvitation.objects.get(from_user=sender, to_user=recipient)
        fsi.accept()
        
        notice.unseen = False
        notice.save()
        
        # send email to notify sender
        ctx = {"sender": sender, "recipient": recipient}
        recipient_first_name = recipient.first_name or "A trendsetter of yours"
        ctx['recipient_first_name'] = recipient_first_name
        if notification:
            notification.send_notification_on("friend-invite-accept", sender=sender, recipient=recipient, recipient_first_name=recipient_first_name)
        else:
            subject = render_to_string(ACCEPT_INVITE_SUBJECT, ctx)
            email_message = render_to_string(ACCEPT_INVITE_MESSGE, ctx)
            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [sender.email])
        
        return redirect(reverse("home"))
#        return redirect(reverse("friend_index"))
    except FriendshipInvitation.DoesNotExist:
        # TODO: need consider about this
        template = "not_authorized.html"
        return direct_to_template(request, template, {})
#        return HttpResponseNotFound()
    except:
        template = "not_authorized.html"
        return direct_to_template(request, template, {})

@login_required
def decline_invitation(request, sender_id, notification_id, template="friends/admirers.html"):
    try:
        fsi = FriendshipInvitation.objects.get(from_user=User.objects.get(pk=sender_id), to_user=request.user)
        fsi.decline()
        notice = Notice.objects.get(pk=notification_id)
        notice.unseen = False
        notice.save()
        #notice.delete()
        return redirect(reverse("home"))
#        return redirect(reverse("friend_index"))
    
    except FriendshipInvitation.DoesNotExist:
        return HttpResponseNotFound()


@login_required
def delete(request, user_id, template="friends/admirers.html"):
    to_user = get_object_or_404(User, pk=user_id)    
    from_user = request.user
    Friendship.objects.remove(from_user, to_user)
    return redirect(reverse("home"))
#    return redirect(reverse("friend_index"))

@json_view
def get_friends(request):
    friends = []
    for obj in Friendship.objects.friends_for_user(request.user):
        friends.append(obj['friend'].first_name)
        friends.append(obj['friend'].last_name)
    return {'friends': friends}
