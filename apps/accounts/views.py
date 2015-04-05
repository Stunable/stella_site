import json 
from django.shortcuts import HttpResponse, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import AccountSettingsForm, WaitlistForm
from apps.accounts.models import UserProfile, AnonymousProfile, Question, QuestionAnswer, Answer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from accounts.forms import AccountCreationForm, AvatarUploadForm,\
    FavouriteDesignerForm, AccountEditForm, ShippingInfoForm,\
    ShippingInfoEditForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
# from django.core.exceptions import ValidationError
from apps.common import get_or_create_profile, json_view
from accounts.models import WaitingList, ShippingInfo, CCToken
from retailers.models import RetailerProfile
from random import random
from django.utils.hashcompat import sha_constructor
from racks.models import Brand, Rack
# from apps.accounts.utils import create_user
from django.conf import settings
from apps.registration.models import RegistrationProfile
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import File
from social_auth.models import UserSocialAuth
from friends.models import Friendship

from apps.kart.models import WishListItem,Cart

from helpers import *

from oauth.oauth import OAuthRequest,OAuthConsumer,OAuthToken,OAuthSignatureMethod_HMAC_SHA1


# import gdata.contacts.data
# import gdata.contacts.client
# import gdata.gauth

    

def check_login(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({'result':True,}, ensure_ascii=False), mimetype='application/json')
    return HttpResponse(json.dumps({'result':False}, ensure_ascii=False), mimetype='application/json')


@login_required
def profile_edit(request, template="accounts/profile_edit.html"):
    ctx = {}

    profile = UserProfile.objects.get(user=request.user)
    ctx['profile'] = profile


    credit_cards = CCToken.objects.filter(user=request.user).order_by('-last_modified')



    ctx['default_ccS']        = credit_cards
    ctx['mode']               = settings.WEPAY_STAGE
    ctx['wepay_client_id']    = settings.WEPAY_CLIENT_ID
    ctx['shipping_form']      = ShippingInfoForm()
    ctx['shipping_addresses'] =ShippingInfo.objects.filter(customer=profile)
    
    
    return direct_to_template(request, template, ctx)




@json_view
@login_required
def avatar_upload(request):
    profile = get_or_create_profile(request)
    if request.method == "POST":
        form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
        form.save()
        
        return {'result': 'ok', 'source': profile.avatar_image.url}
    else:
        return {'result': 'error', 'error': "Errors Occur!"}
#        raise ValidationError("Errors Occur!")






def connect(request):
    """
        Handles incoming calls from Facebook and Google Oauth

        Configured by settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL

    """
    print 'connecting'

    P = None
    try:
        P = request.user.get_profile()
    except:
        P = UserProfile.objects.create(user=request.user)


    # yes this is bad, but we'll improve it later
    for backend in request.user.social_auth.all():

        if backend.provider == 'facebook':

            sa = backend
            
            friends = get_facebook_friends(sa)
                      
            I = get_fb_avatar_image(sa)
            if I:
                try: 
                    temp = NamedTemporaryFile(delete=True)
                    I.save(temp.name+str(P.id),'jpeg')
                    P.avatar.save("%d_avatar.jpg"%P.id, File(open(temp.name+str(P.id),'rb')))
                    P.first_login = False
                    P.save()
                except:
                    pass

            fb_friend_users = {}
            fb_stunable_friends = []
            for u in UserSocialAuth.objects.filter(provider='facebook',uid__in=[f['id'] for f in friends]):
                if not Friendship.objects.are_friends(request.user,u.user):
                    f = Friendship.objects.create(from_user=request.user,to_user=u.user)
                fb_friend_users[u.uid] = u.user

            for index,f in enumerate(friends):
                if f['id'] in fb_friend_users.keys():
                    f['user'] = fb_friend_users[f['id']]
                    fb_stunable_friends.append(f)
                    friends.pop(index)


            request.session['fb_friends'] = friends
            request.session['fb_stunable_friends'] = fb_stunable_friends
            request.session['fb_token'] = sa.tokens['access_token']


        if backend.provider == 'google-oauth2':
            try:
                I = get_google_avatar_image(backend)
                if I:
                    try: 
                        temp = NamedTemporaryFile(delete=True)
                        I.save(temp.name+str(P.id),'jpeg')
                        P.avatar.save("%d_avatar.jpg"%P.id, File(open(temp.name+str(P.id),'rb')))
                        P.first_login = False
                        P.save()
                    except:
                        pass
            except:
                pass

    if request.session.has_key('next'):
        try:
            print 'accounts/connect redirecting to'+request.session.get('next')
            return redirect(request.session.get('next','/'))
        except Exception, e:
            print 'accounts/connect error:',e
    return redirect('/')



