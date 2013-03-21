import json
import urllib2
import time
import datetime
from django.db.models import Q
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from apps.racks.forms import *
from friends.models import Friendship
from django.contrib.auth.models import User
from apps.racks.models import Rack, Rack_Item, Item, Category,ProductImage,ItemType,DailySpecial
from django.contrib import messages
from django.shortcuts import get_object_or_404
from apps.friends.views import json_view
from django.conf import settings
from django.utils import simplejson
from apps.common import get_or_create_profile
import datetime
from tagging.models import Tag,TaggedItem
from voting.models import Vote
from django.views.decorators.cache import cache_page
from django.forms import ValidationError
from notification.models import Notice
from accounts.models import UserProfile
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory
from racks.models import PriceCategory
from social_auth.models import UserSocialAuth
import urllib

from apps.retailers.models import RetailerProfile

from apps.kart.models import WishListItem,KartItem


import random

import logging
logger = logging.getLogger('stunable_debug')

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def gethome(request):
    try:
        RetailerProfile.objects.get(user=request.user)
        return redirect(reverse("retailer_information"))
    except:
        return _all(request)


def get_context_variables(ctx, request):

    if request.user.is_authenticated():
        ctx['tags'] = Tag.objects.get_for_object(request.user) 
        # profile = get_or_create_profile(request)
    else:
        ctx['tags'] = Tag.objects.filter(is_default=True) 
           #print profile.first_login
    
    return ctx

@login_required
def detail(request, rack_id, template='racks/rack_detail.html'):
    ctx = {}
    rack = get_object_or_404(Rack, pk=rack_id)
    user = request.user
    
    # Temporary let user view every rack 
    if True or user == rack.user or user in rack.shared_users.all() or rack.is_public():
        private_racks = Rack.objects.PrivateRacksForUser(user)
        shared_racks = Rack.objects.SharedRacksForUser(user)
        ctx['rack'] = rack
        
        if request.method == 'GET':
            order_by = request.GET.get('order_by')
            q = request.GET.get('q')
            
            if order_by == 'brand-ascending':
                items = rack.rack_items.all().order_by('brand')
#                rack_items = Rack_Item.objects.filter(rack=rack).order_by('item__brand')
            elif order_by == 'brand-descending':
                items = rack.rack_items.all().order_by('-brand')
#                rack_items = Rack_Item.objects.filter(rack=rack).order_by('-item__brand')
            elif order_by == 'price-ascending':
                items = rack.rack_items.all().order_by('price')
#                rack_items = Rack_Item.objects.filter(rack=rack).order_by('item__price')
            elif order_by == 'price-descending':
                items = rack.rack_items.all().order_by('-price')
#                rack_items = Rack_Item.objects.filter(rack=rack).order_by('-item__price')
            else:
                items = rack.rack_items.all()
            
            if q:
                items = items.filter(Q(brand__icontains=q)|Q(name__icontains=q))
            
            ctx['order_by'] = order_by
            ctx['items'] = items
        
        # find shared admirers
        shared_admirers = rack.shared_users.all()
        
        # find non shared admirers
        friendship_list = Friendship.objects.friends_for_user(rack.user)
        friend_list = []
        for friendship in friendship_list:
            friend_list.append(friendship['friend'])
        
        for shared_admirer in shared_admirers:
            if shared_admirer in friend_list:
                friend_list.remove(shared_admirer)
           
        if shared_admirers:
            ctx['racks'] = shared_racks
            ctx['is_private'] = False
            ctx['shared_admirers'] = shared_admirers
            ctx['friends'] = friend_list
        else:
            ctx['racks'] = private_racks
            ctx['is_private'] = True
        
        # rack share with you
        ctx['racks_shared_with_you'] = Rack.objects.RacksSharedWithUser(user)
    else:
        pass
#        messages.error(request, "Not authorized")    
    return direct_to_template(request, template, ctx)

@login_required
def trendsetters(request, user_id=None, template='racks/trendsetters.html'):
    user = request.user
    rack_user = user
    if user_id:
        requested_user = User.objects.get(id=user_id)
        if Friendship.objects.are_friends(user,requested_user):
            rack_user = User.objects.get(id=user_id)

    if rack_user == user:
        racks = Rack.objects.filter(Q(shared_users__in=[rack_user, ]) | Q(publicity=Rack.PUBLIC, user=rack_user.id) | 
                                    Q(publicity=Rack.PRIVATE, user=rack_user.id))
    else:
        racks = Rack.objects.filter(Q(shared_users__in=[requested_user, ]) | Q(publicity=Rack.PUBLIC, user=requested_user.id)) 
    
    ctx = {'trendsetter': rack_user, 'racks': racks}
    return direct_to_template(request, template, ctx)


def wishlist(request):
    if request.user.is_authenticated():
        qs = WishListItem.objects.select_related('item','item_variation','item___retailer','item__featured_image').filter(user=request.user)
    elif settings.DEBUG:
        qs = WishListItem.objects.select_related('item','item_variation','item___retailer','item__featured_image').all()
    else:
        qs = WishListItem.objects.none()

    return _all(request,template='racks/wishlist.html',query_set=qs,is_wishlist=True)


def friends(request):
    qs = WishListItem.objects.none()

    return _all(request,template='racks/friends.html',query_set=qs,is_wishlist=True)

@login_required
def index(request, template='racks/closet.html'):
    ctx = {}
    user = request.user
    ctx['private_racks'] = Rack.objects.PrivateRacksForUser(user)
    
    return direct_to_template(request, template, ctx)

@login_required
def shared(request, template='racks/shared_closet.html'):
    ctx = {}
    user = request.user
    ctx['shared_racks'] = Rack.objects.SharedRacksForUser(user)
    
    # rack share with you
    ctx['racks_shared_with_you'] = Rack.objects.RacksSharedWithUser(user)
    
    return direct_to_template(request, template, ctx)

@login_required
def public(request, template='racks/public.html'):
    ctx = {}
    public_racks = Rack.objects.filter(publicity = Rack.PUBLIC)
    ctx['public_racks'] = public_racks
    return direct_to_template(request, template, ctx)


@login_required
def add(request, template='racks/add.html'):
    if request.is_ajax():
        ctx = {}
        is_public = request.GET.get('public')
        if request.method == 'POST':
            form = RackForm(request.user, request.POST)
            if form.is_valid():            
                rack = form.save(commit = False)
                rack.user = request.user
                if request.POST.get('public') == 'True':
                    rack.publicity = 1
                    target = '.public-racks'
                else:
                    rack.publicity = 0 #default publicity is private
                    target = '.private-racks'
                rack.save()
                # add notification for created rack
                user_friends = Friendship.objects.friends_for_user(request.user)
                
                
                if notification:
                    for friend in user_friends:                    
                        notification.send([friend['friend']], "friend_creates_new_rack", {"rack": rack}, True, request.user)
                
                ctx['success'] = True
                d  = {'rack':rack}
                ctx['result'] = {'html':render_to_string("racks/includes/rack_in_list.html", d),'target':target}
               #print 'ctx:',ctx

                json = simplejson.dumps(ctx)
                return HttpResponse(json, mimetype='application/json')
                 
        else:
            form = RackForm()
        ctx['form'] = form
        ctx['public'] = is_public
        return direct_to_template(request, template, ctx)
    else:
        raise ValidationError('no good...')
        return redirect(reverse("shop"))

@json_view
@login_required
def rack_item_remove(request, rack_id, rack_item_id, template='racks/rack_detail.html'):
    try:
        if request.method == 'POST':
            rack_items = Rack_Item.objects.filter(rack__id=rack_id, item__id=rack_item_id, user=request.user)
            rack_items[0].delete()
            return {'result': True,'callback':'remove'}
    except:
        return {'result': False, 'message':'Item or rack is not valid'}
    
    return {'result': False, 'message':'Method not supported'}

@login_required
def rack_item_add_new(request, rack_id, template='racks/add_item.html'):
    pass

@login_required
def delete(request, rack_id, template="racks/closet.html"):
    #rack = Rack.objects.(pk=rack_id)
    rack = get_object_or_404(Rack, pk=rack_id)
    if request.user == rack.user:   
        rack.delete()
        messages.info(request, "Rack has been deleted successfully")
        ret = {'success': True}
    else:
        messages.error(request, "Not authorized")
        ret = {'success': False}
    
    if request.is_ajax():
        return HttpResponse(json.dumps(ret), mimetype="application/json")
    
    return redirect(reverse("all"))

@login_required
def share_modal_view(request, rack_id, template="racks/share_rack_modal.html"):
    ctx = {}
    rack = get_object_or_404(Rack, pk=rack_id)
    shared_admirers = rack.shared_users.all()        
    # find non shared admirers
    friendship_list = Friendship.objects.friends_for_user(rack.user)
    friend_list = []
    for friendship in friendship_list:
        friend_list.append(friendship['friend'])
        
    for shared_admirer in shared_admirers:
        if shared_admirer in friend_list:
            friend_list.remove(shared_admirer)
           
    ctx['shared_admirers'] = shared_admirers
    ctx['friends'] = friend_list
    ctx['rack'] = rack
    return direct_to_template(request, template, ctx)

RACK_SHARED_SUBJECT = "racks/rack_shared_subject.txt"
RACK_SHARED_MESSAGE = "racks/rack_shared_message.txt"

@json_view
@login_required
def share(request, rack_id, template="racks/share_rack_modal.html"):
    ctx = {}
    rack = get_object_or_404(Rack, pk=rack_id)
    json = simplejson.loads(request.GET.get('json', '[]'))
    user_friendship_list = Friendship.objects.friends_for_user(request.user)
    admirers = []
    if json:
        for admirer_pk in json['share_list']:
            admirer = User.objects.get(pk=int(admirer_pk))
            admirers.append(admirer)
            rack.shared_users.add(admirer)
            
            admirer_friendship_list = Friendship.objects.friends_for_user(admirer)

            # add Trendser shares rack with another trendsetter notification
            for fs_u in admirer_friendship_list:
                for f in user_friendship_list:
                    if f['friend'] == fs_u['friend']:
                        notification.send([f['friend']], "friend_share_rack_with_others", {'send': request.user, 'rack': rack, 'receive': admirer}, True, request.user)
            
            rack_url = u"http://%s%s" % (
                unicode(Site.objects.get_current()),
                unicode(reverse("racks_detail", args=[rack.id]))
            )
            # add share rack notification here
            if notification:
                notification.send([admirer], "trend_received", {"rack": rack}, True, request.user)
                notification.send_notification_on("share-rack", sender=request.user, recipient=admirer, rack_url=rack_url)
            
            # this is really strange... the only reason the following would execute
            # is if the "notification" app was not in installed apps.... which it IS... so... i dunno.
            else:
                ctx = {'sender': request.user, "recipient": admirer, "rack_url": rack_url}
                subject = render_to_string(RACK_SHARED_SUBJECT, ctx)
                email_message = render_to_string(RACK_SHARED_MESSAGE, ctx)
                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [admirer.email])
                
            rack.save()
        
        # if user sign up/ login using facebook
        # send facebook notification only once!
        
        # # TODO: cannot post on user news feed. Maybe Facebook bug!  
        # social_users = UserSocialAuth.objects.filter(provider='facebook').filter(user=request.user)
        # if social_users and admirers:
        #     social_user = social_users[0]
        #     access_token = social_user.tokens['access_token']
        #     # get user friends
        #     url = 'https://graph.facebook.com/me/feed?method=post&client_id=' + settings.FACEBOOK_APP_ID + '&access_token=' + access_token
        #     message = request.user.first_name + ' ' + request.user.last_name + ' shared ' + rack.name.upper() + ' with '
            
        #     for i, admirer in enumerate(admirers):
        #         if i == len(admirers)-1:
        #             name = admirer.first_name + ' ' + admirer.last_name
        #         else:
        #             name = admirer.first_name + ' ' + admirer.last_name + ', '
        #         message += name
                
        #     publish = {
        #       'message': message
        #     };
        #     data = urllib.urlencode(publish)
            
        #     try:
        #         req = urllib2.Request(url, data) 
        #         content = urllib2.urlopen(req)
        #         data = json.load(content)
        #     except:
        #         # TODO: log bug here
        #         pass            
            
    else:
        raise Exception("Please Enter Rack Name")
    return {'result': 'ok'}

@login_required
def edit(request, rack_id, template="racks/edit.html"):
    ctx = {}
    initial_data = {}
    #current_rack = Rack.objects.get(pk=rack_id)
    current_rack = get_object_or_404(Rack, pk=rack_id)
    initial_data.update(vars(current_rack))
    if request.user == current_rack.user:
        if request.method == 'POST':
            form = RackEditForm(request.user, request.POST)
            if form.is_valid():            
                new_name = form.cleaned_data['name']
                if current_rack.name != new_name:
                    current_rack.name = new_name
                current_rack.save()
                if form.cleaned_data['rack_items']:
                    for item in form.cleaned_data['rack_items']:
                        for pre_item in current_rack.rack_items.all():
                            if pre_item not in form.cleaned_data['rack_items']:
                                delete_rack_item = Rack_Item.objects.get(rack=current_rack, item=pre_item)
                                delete_rack_item.delete()                        
                        try:
                            rack_item = Rack_Item.objects.get(rack = current_rack, item = item)
                        except Rack_Item.DoesNotExist:
                            rack_item = Rack_Item(rack = current_rack, item=item)
                            rack_item.save()
                else:
                    for pre_item in current_rack.rack_items.all():
                        delete_rack_item = Rack_Item.objects.get(rack = current_rack, item = pre_item)
                        delete_rack_item.delete()
                
                if form.cleaned_data['shared_users']:                    
                    for user in form.cleaned_data['shared_users']:
                        for pre_user in current_rack.shared_users.all():
                            if pre_user not in form.cleaned_data['shared_users']:
                                current_rack.shared_users.remove(pre_user)
                        current_rack.shared_users.add(user)
                else:
                    for pre_user in current_rack.shared_users.all():
                        current_rack.shared_users.remove(pre_user)
                current_rack.save()
                ctx['success'] = True
                messages.info(request, "Rack has been changed")
                #return redirect(reverse('list_shared_racks'))
                return redirect(reverse('racks_detail', args=[current_rack.id, ]))
        else:
            form = RackEditForm(initial={'name': current_rack.name,
                                     'shared_users': current_rack.shared_users.all(),\
                                     'rack_items': current_rack.rack_items.all()})
             
            friend_list = [friendship['friend'].username for friendship in Friendship.objects.friends_for_user(request.user)]
            form.fields["shared_users"].queryset = User.objects.filter(username__in=friend_list)  
        
        ctx['form'] = form
    else:
        messages.error(request, "Not authorized")
    return direct_to_template(request, template, ctx)

@login_required
def add_admirer(request, rack_id, friend_id, template='racks/rack_detail.html'):
    add_admirer = get_object_or_404(User, pk=friend_id)
    current_rack = get_object_or_404(Rack, pk=rack_id)
    if request.user == current_rack.user:
        current_rack.shared_users.add(add_admirer)     
        current_rack.save()
        messages.info(request, "Admirer has been added successfully")
    else:
        messages.error(request, "Not authorized")
    return redirect("racks_detail", rack_id = rack_id)

@login_required
def remove_admirer(request, rack_id, friend_id, template='racks/rack_detail.html'):
    current_rack = get_object_or_404(Rack, pk=rack_id)
    if request.user == current_rack.user:
        #check of friend exist or not
        current_rack.shared_users.remove(friend_id)
        current_rack.save()
        messages.info(request, "Admirer has been remove successfully")
    else:
        messages.error(request, "Not authorized")
    return redirect("racks_detail", rack_id = rack_id)

@login_required
def item(request, template='racks/item_management.html'):
    item_list = Item.objects.all()
    ctx = {'item_list': item_list}
    return direct_to_template(request, template, ctx)



def variation_modal(request,wishlist_item_id, template='racks/item_modal.html'):

    print 'VARIATION MODAL'

    iv = WishListItem.objects.select_related('item').get(id=wishlist_item_id)
    item = iv.item

    return item_modal(request, item.slug,ctx={'wished_variation':iv})

#@login_required
def item_modal(request, item_slug, template='racks/item_modal.html', ctx=None):
    
    if not ctx:
        ctx = {}
    
    item = get_object_or_404(Item, slug=item_slug)
    ctx['item'] = item

    ctx.update({
                'variations_by_size': item.types.select_related('size').filter(inventory__gte=1).order_by('size'),
                'variations_by_color': item.types.select_related('size').filter(inventory__gte=1).order_by('custom_color_name')
                }) 
               
    if request.is_ajax():
        return direct_to_template(request, template, ctx)

    return _all(request,ctx=ctx)

def divide_into_list(list_item):
    # first_value = 0
    # last_value = 3
    # rack_items_list = []
    
    # c = 0
    
    # while first_value < len(list_item):
    #     list_3_items = list_item[first_value:last_value]
    #     rack_items_list.append(list_3_items)
    #     first_value += 3
    #     last_value += 3
    
    #     # for dev only to prevent loading too much data
    #     c += 1
    #     if c > 20:
    #         break
    
    return list_item

# @login_required
def carousel(request, slug, template='racks/new_carousel.html'):
    ctx = {}
    # profile = get_or_create_profile(request)
    

    current_tag = get_object_or_404(Tag, slug=slug)
    ctx['current'] = current_tag.slug
    get_context_variables(ctx, request)
    
    # if settings.IS_PROD:
    #     query_set = Item.objects.filter(category=current_category, approved=True)
    # else:
    #     query_set = Item.objects.filter(category=current_category)  
    query_set = Item.objects.with_any(current_tag).filter(approved=True,is_available=True)
    
    return pagination(request, ctx, template, query_set)

@json_view
# @login_required
def tab_handler(request, slug, method=None):
    if request.method == 'POST':
        current_tag = get_object_or_404(Tag, slug=slug)

        
        if method=='remove':
            Ts = Tag.objects.get_for_object(request.user).filter(slug=slug)
            for T in Ts:
                TaggedItem.objects.get(tag=T,content_type=ContentType.objects.get_for_model(User),object_id=request.user.id).delete()
            return {'callback':'remove'}
        if method=='add':
            T = Tag.objects.get(slug=slug)
            TI,created = TaggedItem.objects.get_or_create(tag=T,content_type=ContentType.objects.get_for_model(User),object_id=request.user.id)
            if created:
                return {'callback':'add_tab','data':render_to_string("racks/includes/tag_tabs.html",{'tags':[T]})}
            else:
                return {}

        return {}

        


@login_required
def stella_choice(request, template='racks/new_carousel.html'):
    ctx = {}
    user = request.user
    ctx['categories'] = Category.objects.all()
    ctx['current'] = "Stella's Choice"
    get_context_variables(ctx, request)
    begin_date = datetime.date.today() - timedelta(days=14)
    
    if len(Friendship.objects.friends_for_user(user)) < 10:
        template = 'racks/carousel_stellas_choice.html'
        return direct_to_template(request, template, ctx)
    else:        
        friends =  [fs['friend'] for fs in Friendship.objects.friends_for_user(request.user)]
        friends.append(request.user)
        
        # leave place to implement the real stella choice logic
        if settings.IS_PROD:
            query_set = Item.objects.filter(created_date__gt=begin_date, approved=True).order_by('order')
        else:
            query_set = Item.objects.filter(created_date__gt=begin_date).order_by('order')
        
#        ctx['user_items'] = items
#        rack_items_list = divide_into_list(items)
#        ctx['rack_items_list'] = rack_items_list
        return pagination(request, ctx, template, query_set)
    
    
def prepare_ctx(query_set, ctx):
    length = query_set.count()
    items = query_set[:4]
    rack_items_list = []

    for i in xrange(0, len(items), 3):
        rack_items_list.append( items[i:i+3])
    
    user_items = []
    for l in rack_items_list:
        user_items.extend([i.pk for i in l])
        
    ctx['user_items'] = Item.objects.filter(pk__in=user_items)
    ctx['item_count'] = length
    ctx['page_count'] = (length + 2)/3
    ctx['rack_items_list'] = rack_items_list


def stylist(request, stylist_id, template="racks/new_carousel.html"):
    ctx = {}

    ctx['current'] = "stylist"
    get_context_variables(ctx, request)
    
    
    query_set = Item.objects.filter(_retailer__id=stylist_id, approved=True,is_available=True)
        
    return pagination(request, ctx, template, query_set)

def new(request, template="racks/new_carousel.html"):
    ctx = {}

    ctx['current'] = "new"
    get_context_variables(ctx, request)
    
    begin_date = datetime.date.today() - timedelta(days=14)
    
    query_set = Item.objects.filter(created_date__gt=begin_date, approved=True,is_available=True).order_by('created_date')
        
    return pagination(request, ctx, template, query_set)



def daily(request, template="racks/new_carousel.html"):
    ctx = {}

    ctx['current'] = "daily"
    get_context_variables(ctx, request)
        

    today = datetime.date.today()

    query_set = DailySpecial.objects.select_related('Item').filter(
        Q(start_date__lte = today,end_date__gte=today)|
        Q(start_date__lte = today,end_date=None)|
        Q(start_date = None,end_date=None)|
        Q(start_date = None,end_date__gte=today)).filter(weekday__contains=str(today.weekday())+',')


    
    #query_set = Item.objects.filter(created_date__gt=begin_date, approved=True,is_available=True).order_by('created_date')
        
    return pagination(request, ctx, template, query_set)
#    return direct_to_template(request, template, ctx)

#@login_required
def _all(request, slug=None, template='racks/new_carousel.html',query_set = None,is_wishlist = False, ctx=None):
    if not ctx:
        ctx = {'is_wishlist':is_wishlist}

    if not query_set:
        
        if request.GET.get('item_id', None):
            linked_item = Item.objects.filter(id=request.GET.get('item_id'))
            query_set =  linked_item #| Item.objects.filter(brand=linked_item[0].brand).filter(~Q(id =linked_item[0].id))
        if slug:
            linked_item = Item.objects.filter(slug=slug)
            query_set =  linked_item #| Item.objects.filter(brand=linked_item[0].brand).filter(~Q(id =linked_item[0].id))

        # profile = None
        

        ctx['current'] = "all"
        
        if not query_set:
            # if settings.IS_PROD:
                #print "PROD"
                # print 'getting items'
                query_set = Item.objects.select_related('featured_image','_retailer').filter(approved=True,is_available=True).order_by('?')
        # else:
            # query_set = Item.objects.all().order_by('?')
    # print len(query_set)

    get_context_variables(ctx, request)
    
    return pagination(request, ctx, template, query_set)
            
#    return direct_to_template(request, template, ctx)

def pagination(request, ctx, template, query_set):
    page = request.GET.get('page')
    item_per_page = int(request.GET.get('item_per_page', '2'))

   
    if request.is_ajax():
        template = 'racks/patial_carousel.html'
        try:
            page = int(page)
        except:
            page = 1
        _from = item_per_page * page
        _to = _from+item_per_page
        if query_set.count() < _to+item_per_page:
            next = 1
        else:
            next = page+1

        ctx['rack_items_list'] = [query_set[_from:_to]]

        ctx['next'] = next   
    else:
        # template = 'racks/new_carousel.html'
        ctx['rack_items_list'] = [query_set[:12]]
    
        ctx['next'] = 3
    ctx['item_per_page'] = 10
            
    return direct_to_template(request, template, ctx)

@json_view
@login_required
def add_item_from_modal(request):
    """
    /rack/add_item?item_id=xx&rack=xxx
    """
    item_id = request.GET.get('item_id', None)
    rack = request.GET.get('rack', None)
    result = {'result': 'ok'}
    
    if item_id and rack:
        item = Item.objects.get(pk=item_id)
        # create a private rack name custom if user do not have any rack
#        if rack.lower()=='custom':            
#            add_to_rack = Rack(name='Custom', user=request.user, publicity=0)
#            add_to_rack.save()
        if rack.lower() == 'myrack':
            try:
                add_to_rack = Rack.objects.get(name="My Rack", user=request.user)
            except Rack.DoesNotExist:
                add_to_rack = Rack(name='My Rack', user=request.user, publicity=0)
                add_to_rack.save()
                result['new_rack_id'] = add_to_rack.id
        else:
            add_to_rack = Rack.objects.get(pk=rack)
        rack_item = Rack_Item(rack=add_to_rack, item=item, user=request.user)
        rack_item.save()
        # add notification for admirers
        user_friends = Friendship.objects.friends_for_user(request.user)
        if notification:
            for fs_u in user_friends:
                notification.send([fs_u['friend']], "friend_adds_item_to_rack", {"rack": add_to_rack, 'item': item}, True, request.user)
    else:
        result['result'] = 'error'
        result['Error'] = 'item or rack is not valid'
#        return {'result': 'error', 'Error': 'item or rack is not valid'}
    return result

ITEM_SHARED_SUBJECT = "racks/item_shared_subject.txt"
ITEM_SHARED_MESSAGE = "racks/item_shared_message.txt"

@json_view
@login_required
def send_item_to_admirer(request):
    admirers = request.GET.getlist('admirer')
    message = request.GET.get('message', None)
    item_id = request.GET.get('item_id', None)
    admirer_type = request.GET.get('admirer_type', None)
    admirer_name = request.GET.get('admirer_name', None)
    user_friendship_list = Friendship.objects.friends_for_user(request.user)
    ads = []

    if item_id and admirers:

        item = get_object_or_404(Item, pk=item_id)
        for admirer in admirers:
            if admirer_type in ['facebook','both']: #if the item was dropped on a facebook friend ui
            #check to see if this facebook user has also logged into stunable using their facebook account
                fb_stunable_users = UserSocialAuth.objects.filter(provider='facebook',uid=admirer)
                if len(fb_stunable_users)>0:
                    to_user = fb_stunable_users[0].user
                else:
                    to_user=None
            else:
                to_user = User.objects.get(pk=admirer)

            if to_user:
               #print 'to user'
                logger.info(to_user)
                # TODO: implement the link to trend here
                trend_url = u"https://%s%s" % (
                    unicode(Site.objects.get_current()),
                    unicode(reverse("auth_login"))
                )
                logger.info(trend_url)
                try:
                    if notification:
                        notification.send([to_user], "share_item", {"item": item, 'text': message}, True, request.user)
                        notification.send_notification_on("share-item", sender=request.user, recipient=to_user, trend_url=trend_url, item=item)
                    else:
                        ctx  = {'sender':request.user, 'recipient': to_user, 'item': item, 'trend_url': trend_url}
                        
                        if admirer_type == 'stunable':# I don't think we have email addresses if this is a facebook friend
                            logger.info('sending email')
                            # send email to notify
                            try:
                                subject = render_to_string(ITEM_SHARED_SUBJECT, ctx)
                                email_message = render_to_string(ITEM_SHARED_MESSAGE, ctx)
                                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [to_user.email])
                            except Exception, e:
                                logger.error(e)
                except Exception, e:
                    logger.error(e)
                    # TODO: log error here
                    pass
                    
                # send notification for users when friends share product with other friends
                admirer_friendship_list = Friendship.objects.friends_for_user(admirer)
                # add Trendser shares rack with another trendsetter notification
                try:
                    for fs_u in admirer_friendship_list:
                        for f in user_friendship_list:
                            if f['friend'] == fs_u['friend']:
                                notification.send([f['friend']], "friend_share_item_with_others", {'send': request.user, 'item': item, 'receive': to_user}, True, request.user)
                except Exception, e:
                    logger.error(e)
            else:
                social_users = UserSocialAuth.objects.filter(provider=admirer_type).filter(user=request.user)
                if social_users and admirer_type == 'facebook':
                    social_user = social_users[0]
                    access_token = social_user.tokens['access_token']
                    # get user friends
                    url = 'https://graph.facebook.com/me/feed?method=post&client_id=' + settings.FACEBOOK_APP_ID + '&access_token=' + access_token+'&'
                    # msg = '%s shared a ' %request.user.get_full_name()
                    # message = msg + item.brand + ' ' + item.name + ' with '
                    # message += admirer_name
                    message = 'come and see more stuff like %s '%({True:'these',False:'this'}[item.name.endswith('s') and not item.name.endswith('ss')])
                    message += item.brand + ' ' + item.name
                    message += ' at Stunable!'
                        
                    publish = {
                      'method': 'feed'#send but then we can only send the link to facebook page
                      ,'link': settings.WWW_ROOT+'racks/carousel/all?item_id='+str(item.id)
                      ,'description': message
                      ,'name':"check out what I found on stunable"
                      ,'to':admirer
                      ,'picture':settings.WWW_ROOT+item.get_image().url.lstrip('/')
                    }
                    return publish
    else:
        raise Exception("Please choose Admirer or input message")
    return {'result': 'ok'}

# view home page with default rack = 5
@login_required
def helper(request):
    delta = request.user.last_login.date() - datetime.datetime.now().date()
    if delta.days < settings.ABSENT_DAYS:
        return carousel(request, settings.DEFAULT_RACK)
    else:
        return redirect(reverse("main-help"))

@login_required
def search(request, template="racks/rack_detail.html"):
    search_string = request.GET.get('q', '')
    filter_by = request.GET.get('filter', '')
    rack_id = request.GET.get('rack_id', '')
    ctx = {}
    rack = get_object_or_404(Rack, pk=rack_id)
    user = request.user
    
    if user == rack.user or user in rack.shared_users.all() or rack.is_public():
        private_racks = Rack.objects.PrivateRacksForUser(user)
        shared_racks = Rack.objects.SharedRacksForUser(user)
        ctx['rack'] = rack
        # find shared admirers
        shared_admirers = rack.shared_users.all()
        
        # find non shared admirers
        friendship_list = Friendship.objects.friends_for_user(rack.user)
        friend_list = []
        for friendship in friendship_list:
            friend_list.append(friendship['friend'])
        
        for shared_admirer in shared_admirers:
            if shared_admirer in friend_list:
                friend_list.remove(shared_admirer)
           
        if shared_admirers:
            ctx['racks'] = shared_racks
            ctx['is_private'] = False
            ctx['shared_admirers'] = shared_admirers
            ctx['friends'] = friend_list
        else:
            ctx['racks'] = private_racks
            ctx['is_private'] = True
        
        # rack share with you
        ctx['racks_shared_with_you'] = Rack.objects.RacksSharedWithUser(user)
    
    if rack_id:        
        from django.db.models import Q
        
        qs = Item.objects.filter(rack_item__rack__pk=rack_id)
                
        search_string = search_string.lower()
        
        if filter_by == "designer":
            qs = qs.filter(rack_item__item__brand__icontains=search_string)
        
        if filter_by == "color":
            qs = qs.filter(rack_item__item__colors__icontains=search_string)

        if filter_by == "category":
            qs = qs.filter(rack_item__item__category__name__icontains=search_string)
        
        if filter_by == "filter_by":
            qs = qs.filter(Q(category__name__icontains=search_string)|Q(colors__icontains=search_string)|Q(brand__icontains=search_string))
    
        ctx['items'] = qs
        
    ctx['searching'] = True
    
    return direct_to_template(request, template, ctx)

@cache_page(60 * 60 * 24)
@json_view
def get_brands(request):
#    brands = [v['brand'] for v in Item.objects.all().distinct('brand').values('brand')]
    brands = [brand.name for brand in Brand.objects.all().distinct("brand")]
    return {'brands': brands}

@login_required
def jean_submit(request, template="racks/bummer.html"):
    # leave place for later implementation
    ctx = {}
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                user_profile = request.user.get_profile()
            except UserProfile.DoesNotExist:
                user_profile = UserProfile(user=request.user)
            user_profile.favourite_designer = form.cleaned_data.get('name')
            user_profile.save()
            return redirect(reverse('home'))
    else:
        form = BrandForm()
    ctx['form'] = form
    return direct_to_template(request, template, ctx)

@login_required
def update_rack_name(request, rack_id, template="racks/rack_detail.html"):
    ctx = {}
    ret = {'success': False}
    rack = get_object_or_404(Rack, pk=rack_id)
    if request.method == "POST":
        form = RackNameEditForm(request.POST, instance=rack)
        if form.is_valid():
            form.save()
            ret['success'] = True
    else:
        form = RackNameEditForm(instance=rack)
    
    if request.is_ajax():
        return HttpResponse(json.dumps(ret), mimetype="application/json")
    
    ctx['form'] = form
    return redirect(reverse("racks_detail", args=[rack_id]))

@login_required
def add_size(request, template="racks/add_size_dialog.html"):
    ctx  = {}
    if request.GET.get('item_id'):        
        ctx['item_id'] = request.GET.get('item_id')
    if request.method == "POST":
        form = AddSizeForm(request.POST)
        if form.is_valid():
            size = form.save(commit=False)
            # only retailers are adding sizes through this form
            size.retailer = request.user
            size.save()
            response_data = {'success': True, 'id': size.pk, 'name': size.size}
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        else:
            error_detail = form.errors.items()[0]
            response_data = {'success': False, 'errors': form.errors, 'message': ': '.join([error_detail[0], ' '.join(error_detail[1])])}
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        form = AddSizeForm()
    
    ctx['form'] = form
    return direct_to_template(request, template, ctx)

@login_required
def add_color(request, template="racks/add_color_dialog.html"):
    ctx  = {}
    if request.GET.get('item_id'):        
        ctx['item_id'] = request.GET.get('item_id')
    if request.method == "POST":
        form = AddColorForm(request.POST)
        if form.is_valid():
            color = form.save(commit=False)
            color.retailer = request.user
            color.save()
            response_data = {'success': True, 'id': color.pk, 'name': color.name}
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        else:
            response_data = {'success': False, 'errors': form.errors}
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        form = AddColorForm()
    
    ctx['form'] = form
    return direct_to_template(request, template, ctx)


def sale_items(request, template="racks/new_carousel.html"):
    ctx = {'current':'sale'}
    query_set=Item.objects.filter(is_onsale=True,is_available=True,approved=True)

    get_context_variables(ctx, request)
    
    return pagination(request, ctx, template, query_set)

def recent_added_items(request, template="racks/item_list.html"):
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    qs = Item.objects.filter(rack_item__created_date__gte=thirty_days_ago)
    ctx = {'items': qs, "title": "recently added"}
    return direct_to_template(request, template, ctx)


@login_required
def purchased_items(request, template="racks/item_list.html"):
    # qs = Item.objects.filter(pk__in=[ci.object_id for ci in KartItem.objects.filter(cart__purchase__purchaser=request.user)])
    ctx = {'items': [], "title": "purchased"}
    return direct_to_template(request, template, ctx)

@login_required
def steal_rack(request, rack_id):
    try:
        rack = Rack.objects.get(pk=rack_id)
        rack_owner = rack.user
        stolen_rack_name = rack.name + ' by ' + (rack_owner.first_name and rack_owner.last_name and (rack_owner.first_name + ' ' + rack_owner.last_name))  
        stolen_rack = Rack(user=request.user, name=stolen_rack_name, publicity=Rack.PUBLIC)
        stolen_rack.save()
        
        for item in rack.rack_items.all():
            Rack_Item(rack=stolen_rack, user=request.user, item=item).save()
                    
        ret = {'success': True, 'created_rack': {'id': stolen_rack.pk, 'name': stolen_rack.name, 'url': reverse('racks_detail', kwargs={'rack_id': stolen_rack.pk})}}
    except Exception, e:
        ret = {'success': False, 'message': e.message}
    
    return HttpResponse(json.dumps(ret), mimetype="application/json")

@login_required
def get_new_notifications(request):
    ret = {'success': True, 'has_new': False}
    try:
        current_time = datetime.datetime.now()
        # get latest notification for current user
        notices = Notice.objects.filter(recipient=request.user, unseen=True).order_by('-added')
        # remove the trend from happnening
        notices = notices.exclude(notice_type__default=7)
        if notices:
            current_time = time.mktime(datetime.datetime.now().timetuple())
            latest_notice_created_time = time.mktime(notices[0].added.timetuple())
            minute_diff = (current_time - latest_notice_created_time)/60
            if minute_diff <= settings.NOTICE_TIME_DIFF:
                ret['has_new'] = True
        else:
            # nothing will happen because there is no new notification
            pass
    except:
        ret['success'] = False
    return HttpResponse(json.dumps(ret), mimetype="application/json")

@login_required
def display_notice_table(request, template="notification/notes.html"):
    notices = Notice.objects.notices_for(request.user)
    # remove the trend from happnening
    notices = notices.exclude(notice_type__default=7)
    return direct_to_template(request, template, {'notes': notices})
