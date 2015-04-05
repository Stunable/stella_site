import json
import urllib2
import time
import datetime
from django.db.models import Q
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# from apps.racks.forms import *
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
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.forms.models import modelform_factory
from racks.models import PriceCategory
from social_auth.models import UserSocialAuth
import urllib

from apps.retailers.models import RetailerProfile

from apps.kart.models import WishListItem,KartItem,Cart
from apps.stunable_search.models import Flavor,UserSearchTab


import random

import logging
logger = logging.getLogger('stunable_debug')

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None




def checkAddTab(function):
    
    def wrap(request, *args, **kwargs):

        if request.GET.get('a',None):
            try:
                m = {
                    'stylist': ('retailers','retailerprofile'),
                    'item_modal': ('racks','item'),
                    'flavor':('stunable_search','flavor')
                }[function.__name__]
                # get the model class
                model = get_model(*m)

                # get its content type
                c = ContentType.objects.get_for_model(model)

                # get the instance of the model class
                obj = model.objects.get(slug=kwargs['slug'])

                # create or get the correct search tab
                t,created = UserSearchTab.objects.get_or_create(content_type=c,object_id=obj.id)

                # add the user to the tab
                if request.user.is_authenticated():
                    t.users.add(request.user)
                else:
                    sesstabs = request.session.get('tabs',[])
                    sesstabs.append(t)
                    request.session['tabs'] = sesstabs
            except:
                pass

            return redirect(reverse(function.__name__,kwargs=kwargs))

        return function(request, *args, **kwargs)


    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def gethome(request):
    try:
        RetailerProfile.objects.get(user=request.user)
        return redirect(reverse("retailer_information"))
    except:
        return _all(request)


def get_context_variables(ctx, request):

    if request.user.is_authenticated():
        ctx['tags'] = request.user.usersearchtab_set.all()
    else:
        ctx['tags'] = [t for t in UserSearchTab.objects.filter(is_default=True)] 
        ctx['tags'] += request.session.get('tabs',[])

    today = datetime.date.today()
    specials = DailySpecial.objects.filter(
        Q(start_date__lte = today,end_date__gte=today)|
        Q(start_date__lte = today,end_date=None)|
        Q(start_date = None,end_date=None)|
        Q(start_date = None,end_date__gte=today)).filter(weekday__contains=str(today.weekday()))
           #print profile.first_login

    ctx['specials'] = specials
    
    return ctx


@login_required
def wishlist(request):

    cart=Cart(request)

    if request.user.is_authenticated():
        qs = WishListItem.objects.select_related('item','item_variation','item___retailer','item__featured_image').filter(user=request.user)
    else:
        qs = WishListItem.objects.select_related('item','item_variation','item___retailer','item__featured_image').filter(cart=cart)

    return _all(request,template='racks/wishlist.html',query_set=qs,is_wishlist=True)


def friends(request):
    qs = request.session.get('fb_friends',[])

    ctx = {'friends':True,'first_page_count':50,'item_per_page':50}

    return _all(request,ctx=ctx,template='racks/friends.html',query_set=qs,is_wishlist=True)


def variation_modal(request,wishlist_item_id, template='racks/item_modal.html'):

    print 'VARIATION MODAL'

    iv = WishListItem.objects.select_related('item').get(id=wishlist_item_id)
    item = iv.item

    return item_modal(request, item.slug,ctx={'wished_variation':iv})

#@login_required
@checkAddTab
def item_modal(request, slug, template='racks/item_modal.html', ctx=None):
    
    if not ctx:
        ctx = {}
    
    item = get_object_or_404(Item, slug=slug)
    ctx['item'] = item

    ctx.update({
                'variations_by_size': item.types.select_related('size').filter(inventory__gte=1,approved=True).order_by('size'),
                'variations_by_color': item.types.select_related('size').filter(inventory__gte=1,approved=True).order_by('custom_color_name')
                }) 
               
    if request.is_ajax() and not request.GET.get('page',None):
        return render(request, template, ctx)

    if request.GET.get('similar',None):
        pass
    else:
        ctx['direct_link_item'] = item
    ctx['current'] = slug
    ctx['object'] = item

    qs = item.get_related(limit=None)


    return _all(request,ctx=ctx,query_set=qs)

def divide_into_list(list_item):    
    return list_item



@checkAddTab
def flavor(request, group, slug, mode=None,template='racks/new_carousel.html'):
    ctx={'current':'all'}


    query_set = Item.objects.with_any(
            get_object_or_404(Flavor, group=group, slug=slug).get_contained_tags()
        ).filter(approved=True,is_available=True)

    get_context_variables(ctx, request)
    
    ctx['current'] = slug
    ctx['object'] = Flavor.objects.get(slug=slug,group=group)
    
    return pagination(request, ctx, template, query_set)


# @login_required
@checkAddTab
def carousel(request, slug, mode=None,template='racks/new_carousel.html'):
    ctx = {'current':'all'}
    # profile = get_or_create_profile(request)
    current_tag = None

   
    try:
        current_tag = DailySpecial.objects.get(slug=slug)
        query_set = current_tag.get_items().filter(approved=True,is_available=True)
    except:
        query_set = Item.objects.carousel_items().select_related('featured_image','_retailer').order_by('?')

    if current_tag:
        ctx['current'] = current_tag.slug
        ctx['object'] = current_tag
    get_context_variables(ctx, request)
    
    return pagination(request, ctx, template, query_set)


# @login_required
def daily(request, slug, mode=None,template='racks/new_carousel.html'):
    ctx = {'current':'all'}
    # profile = get_or_create_profile(request)
    current_tag = None

    current_tag = DailySpecial.objects.get(slug=slug)
    query_set = current_tag.get_items().filter(approved=True,is_available=True)
   
    if current_tag:
        ctx['current'] = current_tag.slug
        ctx['object'] = current_tag
    get_context_variables(ctx, request)
    
    return pagination(request, ctx, template, query_set)


@json_view
# @login_required
def tab_handler(request, slug, method=None):
    if request.method == 'POST':
        current_tag = get_object_or_404(UserSearchTab, slug=slug)
    
        if method=='remove':
            current_tag.users.remove(request.user)
            return {'callback':'remove'}
        if method=='add':
            T = Tag.objects.get(slug=slug)
            TI,created = TaggedItem.objects.get_or_create(tag=T,content_type=ContentType.objects.get_for_model(User),object_id=request.user.id)
            if created:
                return {'callback':'add_tab','data':render_to_string("racks/includes/tag_tabs.html",{'tags':[T]})}
            else:
                return {}

        return {}

@checkAddTab
def stylist(request, slug, template="racks/new_carousel.html"):
    ctx = {}

    get_context_variables(ctx, request)

    try:
        retailer = RetailerProfile.objects.get(slug=slug)
        query_set = retailer.get_items()
    except:
        retailer = RetailerProfile.objects.none()
        query_set = Item.objects.none()
    
    
    

    ctx['current'] = slug
    ctx['object'] = retailer
        
    return pagination(request, ctx, template, query_set)

def new(request, template="racks/new_carousel.html"):
    ctx = {}

    ctx['current'] = "new"
    get_context_variables(ctx, request)    
    query_set = Item.objects.carousel_items().order_by('created_date')
    ctx['object'] = query_set[0]
        
    return pagination(request, ctx, template, query_set)


#@login_required
def _all(request, slug=None, template='racks/new_carousel.html',query_set = None,is_wishlist = False, ctx=None, all_items=False):
    if not ctx:
        ctx = {'is_wishlist':is_wishlist}

    get_context_variables(ctx, request)

    
    if query_set is None:
        if ctx.has_key('specials'):
            if len(ctx['specials']):
                ctx['current'] = ctx['specials'][0].slug
                query_set = ctx['specials'][0].get_items()
                ctx['object'] = query_set[0]
        
        if query_set is None:
            if request.GET.get('item_id', None):
                linked_item = Item.objects.filter(id=request.GET.get('item_id'))
                query_set =  linked_item #| Item.objects.filter(brand=linked_item[0].brand).filter(~Q(id =linked_item[0].id))
            if slug:
                linked_item = Item.objects.filter(slug=slug)
                query_set =  linked_item #| Item.objects.filter(brand=linked_item[0].brand).filter(~Q(id =linked_item[0].id))

        # profile = None

        if all_items or query_set is None:
            query_set = Item.objects.carousel_items().select_related('featured_image','_retailer').order_by('?')
            if not ctx.has_key('current'):
                ctx['current'] = "all"


    
    return pagination(request, ctx, template, query_set)
            
#    return render(request, template, ctx)

def pagination(request, ctx, template, query_set):
    page = request.GET.get('page')
    item_per_page = int(request.GET.get('item_per_page', '2'))

   
    if request.is_ajax():
        template = 'racks/patial_carousel.html'
        if ctx.has_key('is_wishlist') and ctx['is_wishlist']:
            template = 'racks/patial_wishlist.html'
        
        if ctx.get('friends',None):
            template = 'racks/patial_friends.html'

        try:
            page = int(page)
        except:
            page = 1


        print 'getting items...'
        _from = item_per_page * page
        _to = _from+item_per_page
        next = page+1
        ctx['rack_items_list'] = query_set[_from:_to]

        ctx['next'] = next   
    else:
        # template = 'racks/new_carousel.html'
        ctx['rack_items_list'] = query_set[:ctx.get('first_page_count',10)]
    
        ctx['next'] = 3

    ctx['item_per_page'] = ctx.get('item_per_page',8)


    if len(ctx['rack_items_list']) < 1:
        if ctx.has_key('object'):
            ctx['more_like_this'] = ctx['object'].get_more()
    else:
        print 'outlist:',ctx['rack_items_list']
        print template
            
    return render(request, template, ctx)



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
    return render(request, template, ctx)


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
    return render(request, template, ctx)

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
    return render(request, template, ctx)


def sale_items(request, template="racks/new_carousel.html"):
    ctx = {'current':'sale'}
    query_set=Item.objects.carousel_items().filter(is_onsale=True)

    get_context_variables(ctx, request)

    ctx['object'] = query_set[0]
    
    return pagination(request, ctx, template, query_set)

def recent_added_items(request, template="racks/item_list.html"):
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    qs = Item.objects.filter(rack_item__created_date__gte=thirty_days_ago)
    ctx = {'items': qs, "title": "recently added"}
    ctx['object'] = qs[0]

    return render(request, template, ctx)


@login_required
def purchased_items(request, template="racks/item_list.html"):
    # qs = Item.objects.filter(pk__in=[ci.object_id for ci in KartItem.objects.filter(cart__purchase__purchaser=request.user)])
    ctx = {'items': [], "title": "purchased"}
    return render(request, template, ctx)

