import json 
import urllib2    
from django.shortcuts import HttpResponse, get_object_or_404
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
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
from django.core.exceptions import ValidationError
from apps.common import get_or_create_profile, json_view
from accounts.models import WaitingList, ShippingInfo, CCToken
from retailers.models import RetailerProfile
from random import random
from django.utils.hashcompat import sha_constructor
from racks.models import Brand, Rack
from apps.accounts.utils import create_user
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

from StringIO import StringIO
from PIL import Image
from django.core.files.temp import NamedTemporaryFile

from oauth.oauth import OAuthRequest,OAuthConsumer,OAuthToken,OAuthSignatureMethod_HMAC_SHA1
import httplib, json, time, datetime

import gdata.contacts.data
import gdata.contacts.client
import gdata.gauth

    
@login_required
def profile_edit(request, template="accounts/profile_edit.html"):
    ctx = {}
    
    #check retailer
    try:
        retailer_profile = RetailerProfile.objects.get(user=request.user)
        if retailer_profile:
            return redirect(reverse("retailer_information", args=[retailer_profile.name, ]))
    except:
        pass
    
    # get shipping_info
    user_profile = request.user.get_profile()
    shipping_infos = ShippingInfo.objects.filter(customer=user_profile)
    
    ctx['shipping_infos'] = shipping_infos
    
    if not request.GET.get("user_id"):
        user = request.user
    else:
        user_id = request.GET.get("user_id")
        user = User.objects.get(pk=user_id)
        # view another user profile
        ctx['is_view'] = True
    
    initial_data = {'email': user.email}
    qas = []
    
    try:
        profile = user.get_profile()
        initial_data.update(vars(profile))
#        if not initial_data.get('zipcode', None):
#            initial_data['zipcode'] = 'optional'
        
        for q in Question.objects.all():
            try:
                answer = QuestionAnswer.objects.get(question=q, profile=profile).answer
            except QuestionAnswer.DoesNotExist:
                answer = None
                
            qas.append({'question': q, 'answer': answer})

    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
        for q in Question.objects.all():
            qas.append({'question': q, 'answer': None})

    ctx['qas']= qas
    ctx['profile']= profile
    
    if request.method == 'POST':        
        form = AccountSettingsForm(request.POST, request.FILES)
        if request.is_ajax():
            response = {'success' : True, 'errors': {}}
            if form.is_valid():
                new_pwd = form.cleaned_data.get('password1')
                if new_pwd:
                    user.set_password(new_pwd)
                    user.save()
                user.first_name = form.cleaned_data.get('firstname')
                user.last_name = form.cleaned_data.get('lastname')
                user.save();
                profile.age_range = form.cleaned_data.get('age_range')
                profile.zipcode = form.cleaned_data.get('zipcode')
                profile.avatar = form.cleaned_data.get('avatar')
                profile.view_happenings = form.cleaned_data.get('view_happenings')
                
                profile.save()
            else:
                response.update({'success' : False})
                response['errors'].update(form.errors)
            return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
    else:
        form = AccountSettingsForm(initial=initial_data)
    
    ctx['form'] = form
    ctx['cc_tokens'] = CCToken.objects.filter(user=request.user)
    return direct_to_template(request, template, ctx)

@login_required
def update_answers(request):
    try:
        profile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    
    if request.method == 'POST':
        for param in request.POST.keys():
            if param.startswith('question_'):
                answer_pk = request.POST.get(param)
                question_pk = int(param.strip('question_'))
                q = Question.objects.get(pk=question_pk)
                a = Answer.objects.get(pk=answer_pk)                
                qa_qs = QuestionAnswer.objects.filter(question=q, profile=profile)
                if qa_qs:
                    qa = qa_qs[0]
                else:
                    qa = QuestionAnswer(question=q, profile=profile)
                qa.answer = a
                qa.save()
                    
    return redirect(reverse('profile_edit'))

def create(request, template="accounts/account_create.html"):
    ctx = {}
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():

            new_user = RegistrationProfile.objects.create_inactive_user(username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                send_email=False,
                profile_callback=None)
            
            new_user.first_name = form.cleaned_data['firstname']
            new_user.last_name = form.cleaned_data['lastname']
            new_user.save()
            try:
                profile = new_user.get_profile()
            except UserProfile.DoesNotExist:
                profile = UserProfile(user=new_user)
                
            profile.age_range = form.cleaned_data.get('age_range')
            if form.cleaned_data.get('zipcode') == 'optional':
                profile.zipcode = ""
            else:
                profile.zipcode = form.cleaned_data.get('zipcode')
            profile.save()
            
            # send email
            current_site = Site.objects.get_current()
            
            subject = render_to_string('registration/activation_email_subject.txt',
                                       { 'site': current_site })
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            
            registration_profile = RegistrationProfile.objects.get(user=new_user)
            
            message = render_to_string('registration/activation_email.txt',
                                       { 'activation_key': registration_profile.activation_key,
                                         'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                         'site': current_site, 'user': new_user })
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
            
            ctx['success'] = True
            return redirect(reverse('create_confirm'))
    else:
        form = AccountCreationForm()
    
    ctx['form'] = form        
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

#@login_required
def welcome(request, template="accounts/welcome.html"):
    ctx = {}
    if request.user.is_authenticated():
        profile = get_or_create_profile(request)

        retailer_profile = RetailerProfile.objects.filter(user=request.user)
        if retailer_profile.count() > 0:
            return redirect(reverse('retailer_information', args=[retailer_profile[0].name, ]))
    else:
        if request.session.has_key('anonymous_profile'):
            profile = request.session.get('anonymous_profile')
        else:
            profile = AnonymousProfile.objects.create()
            request.session['anonymous_profile'] = profile
    
    
    if not profile.favourite_designer:
        if request.method == "POST":
            form = FavouriteDesignerForm(request.POST, instance=profile)
            if form.is_valid():
                profile = form.save()
                print profile.favourite_designer

                if profile.first_login:
                    # create two default racks for first time login user
                    for rack in settings.INITIAL_RACKS:
                        r = Rack.objects.create(name=rack, publicity=1)
                        r.owner = profile
                        r.save()

                    profile.first_login = False
                    profile.save()
                
                if profile.favourite_designer: 
                    try:
                        product_group = Brand.get_product_group_from_brand(profile.favourite_designer)
                        profile.update_product_group_tag(product_group)                    
                    except:
                        raise
                if not request.user.is_authenticated():
                    request.session['anonymous_profile'] = profile
                ctx['success'] = True
                return redirect(reverse('home'))
        else:
            form = FavouriteDesignerForm()
        ctx['form'] = form
        return direct_to_template(request, template, ctx)
    return redirect(reverse('home'))

def invite_waitlist(request, template="accounts/request_invite.html"):
    ctx = {}
    if request.method == "POST":
        form = WaitlistForm(request.POST)
        if form.is_valid():
            form.save()
            ctx['success'] = True
            template = "accounts/thank-you.html"
    else:        
        form = WaitlistForm()
    
    ctx['form']=form
    return direct_to_template(request, template, ctx)

def new_user_join(request, confirmation_key, template="friends/admirers.html"):
    try:
        nj = WaitingList.objects.get(confirmation_key = confirmation_key)
        #create new user with random password
        password = sha_constructor(str(random())).hexdigest()[:5]
        user = User(email=nj.email, username=nj.email)
        user.is_active = True
        user.set_password(password)
        user.save()
        user = authenticate(username=user.email, password=password)
        login(request, user)
        profile = get_or_create_profile(request)
#        if request.user.vote_set.all().count() == 0:
#            request.session['first_time_login'] = True
        return redirect(reverse("accounts.urls.profile_edit"))
    except:
        # click on invitation link the second time forward
#        user = User.objects.get(email=nj.email)
        return redirect(reverse("auth_login"))
    
    return direct_to_template(request, template, {})

def login_with_fb(request):
    return HttpResponseRedirect(reverse('socialauth_begin', args=['facebook',]))

@login_required
def make_default(request, info_id):
    shipping_info = get_object_or_404(ShippingInfo, pk=info_id)
    try:
        default_shipping_infos = ShippingInfo.objects.filter(customer=request.user.get_profile(), is_default=True)
        if default_shipping_infos.count() > 0:
            for info in default_shipping_infos:
                info.is_default = False
                info.save()
        
        # mark new shipping info as default
        shipping_info.is_default = True
        shipping_info.save()
    except:
        pass
    return redirect(reverse("profile_edit"))

@login_required
def update_shipping_info(request, info_id):
    ctx = {}
    current_shipping_info = get_object_or_404(ShippingInfo, pk=info_id)
    if request.method == "POST":
        form = ShippingInfoEditForm(request.POST, instance=current_shipping_info)
        if form.is_valid():
            form.save()
    else:
        form = ShippingInfoEditForm(instance=current_shipping_info)
    
    ctx['form'] = form
    return redirect(reverse("profile_edit"))

@login_required
def create_new_shipping_info(request, template="accounts/add_shipping_info_dialog.html"):
    ctx = {}
    try:
        user_profile = request.user.get_profile()
    except:
        user_profile = None
    if request.method == "POST":
        form = ShippingInfoForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': True}
        else:
            error_detail = form.errors.items()[0]
            response_data = {'success': False, 'message': form.errors, 'message': ': '.join([error_detail[0], ' '.join(error_detail[1])])}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
#            return redirect(reverse("profile_edit"))
    else:
        form = ShippingInfoForm(initial={'customer':user_profile})
    
    ctx['form'] = form
    return direct_to_template(request, template, ctx)

def add_fb_friends_to_list(list, js):
    if js.get('paging'):
        if js.get('paging').get('next'):
            req = urllib2.Request(url=js['paging']['next'])
            content = urllib2.urlopen(req)
            js = json.load(content)
            for x in xrange(0, len(js['data'])):
                list.append(js['data'][x])
            add_fb_friends_to_list(list, js)


def connect(request):
    print 'connecting'
    for sa in request.user.social_auth.filter(provider='facebook'):
        friends = get_facebook_friends(sa)
        P = None
        try:
            P = request.user.get_profile()
        except:
            P = UserProfile.objects.create(user=request.user)
            P.set_default_tags()


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
    if request.session.has_key('next'):
        try:
            print 'accounts/connect redirecting to'+request.session.get('next')
            return redirect(request.session.get('next','/'))
        except Exception, e:
            print 'accounts/connect error:',e
    return redirect('/')

# connection = httplib.HTTPSConnection('api.twitter.com')


def request(url, access_token, parameters=None):
    """
    usage: request( '/url/', your_access_token, parameters=dict() )
    Returns a OAuthRequest object
    """
    token = OAuthToken(access_token['oauth_token'], access_token['oauth_token_secret'])
    consumer = OAuthConsumer(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    oauth_request = OAuthRequest.from_consumer_and_token(consumer, token=token, http_url=url, parameters=parameters,
    )
    oauth_request.sign_request(OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
    return oauth_request

def fetch_response(oauth_request, connection):
    url = oauth_request.to_url()
    connection.request(oauth_request.http_method,url)
    response = connection.getresponse()
    s = response.read()
    return s

# def get_twitter_contacts(social_user):
#     print social_user.tokens
    
#     oauth_request = request('https://api.twitter.com/1/friends/ids.json', social_user.tokens)
#     json = fetch_response(oauth_request, connection)
#     print json
#     return json


# def get_google_contacts(social_user):
#     access_token = social_user.tokens['access_token']

#     contacts = []

#     gd_client = gdata.contacts.client.ContactsClient()
#     feed = gd_client.get_contacts(auth_token=gdata.gauth.AuthSubToken(access_token))
#     for i, entry in enumerate(feed.entry):
#         print entry
#         out = {}
#         if hasattr(entry,'name'):
#             if hasattr(entry.name,'full_name'):
#                 out['full_name'] = entry.name.full_name.text

#         for email in entry.email:
#             if email.primary:
#                 out['email'] = email.address

#                 contacts.append(out)
#     print contacts

def get_fb_avatar_image(social_user):
    access_token = social_user.tokens['access_token']
    url = 'https://graph.facebook.com/me/?access_token=' + access_token
    req = urllib2.Request(url=url)
    content = urllib2.urlopen(req)
    d = json.loads(content.read())

    url = 'https://graph.facebook.com/me/picture?access_token=' + access_token
    print url
    req = urllib2.Request(url=url)
    content = urllib2.urlopen(req)
    I = Image.open(StringIO(content.read()))
    return I
   


def get_facebook_friends(social_user):

    access_token = social_user.tokens['access_token']
    
    # get user friends
    url = 'https://graph.facebook.com/me/friends?access_token=' + access_token
    req = urllib2.Request(url=url)
    content = urllib2.urlopen(req)
    fb_friends = json.load(content)
    friend_list = []
    id_list = []
    
    
    for x in xrange(0, len(fb_friends['data'])):
        friend_list.append(fb_friends['data'][x])

    add_fb_friends_to_list(friend_list, fb_friends)

    return friend_list


def add_facebook_friend(request, template="accounts/add_facebook_friends.html"):
    try:
        if len(Friendship.objects.friends_for_user(request.user)) > 0:
            return redirect(reverse("home"))
        else:
            social_user = UserSocialAuth.objects.filter(provider='facebook').get(user=request.user)
            access_token = social_user.tokens['access_token']
            
            # get user friends
            url = 'https://graph.facebook.com/me/friends?access_token=' + access_token
            req = urllib2.Request(url=url)
            content = urllib2.urlopen(req)
            fb_friends = json.load(content)
            friend_list = []
            id_list = []
            
            
            for x in xrange(0, len(fb_friends['data'])):
                friend_list.append(fb_friends['data'][x])
                
            add_fb_friends_to_list(friend_list, fb_friends)
            
            return fb_friends
            
            # return direct_to_template(request, template, {'fb_friends': friend_list, 
            #                                               'access_token': access_token, 
            #                                               'uid': social_user.uid,
            #                                               'FB_APP_ID': settings.FACEBOOK_APP_ID})
    except:
        raise

@login_required
@csrf_exempt
def update_profile(request, template="accounts/profile_edit.html"):
    ctx = {}
    try:
        profile = UserProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = AccountEditForm(request.POST, instance=profile)
            if form.is_valid():
                user = request.user
                # TODO: check and fix bug here
                if form.cleaned_data.get('email'):
                    user.email = form.cleaned_data.get('email')
                    profile.user.email = form.cleaned_data.get('email')
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data.get('password'))
                if form.cleaned_data.get('first_name'):
                    user.first_name = form.cleaned_data.get('first_name')
                    profile.user.first_name = form.cleaned_data.get('first_name')
                if form.cleaned_data.get('last_name'):
                    user.last_name = form.cleaned_data.get('last_name')
                    profile.user.last_name = form.cleaned_data.get('last_name')
                
                form.save()
                user.save()
                profile.save()
                
                if request.session.get("first_time_login"):
                    return redirect(reverse("home"))
        else:
            form = AccountEditForm(instance=profile)
        
        ctx['form']=form
        ctx['profile'] = profile
        
        # get shipping_info
        user_profile = request.user.get_profile()
        shipping_infos = ShippingInfo.objects.filter(customer=user_profile)
        
        ctx['shipping_infos'] = shipping_infos
    except:
        pass
    
    ctx['cc_tokens'] = CCToken.objects.filter(user=request.user)
    
    return direct_to_template(request, template, ctx)

@login_required
def cc_set_default(request, id):
    for cct in CCToken.objects.all():
        cct.is_default=False
        cct.save()
    
    cc_token = CCToken.objects.get(id=id)
    cc_token.is_default=True
    cc_token.save()

    return HttpResponseRedirect('/accounts/profile')
    
    

