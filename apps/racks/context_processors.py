from racks.models import Rack
from friends.models import Friendship
from notification.models import Notice
from cart.cart import Cart
import random
from django.conf import settings

def racks(request):
    context = {}
    user = request.user
    if not user.is_authenticated():
        context['public_racks'] = Rack.objects.filter(anon_user_profile=request.session.get('anonymous_profile'))
        return context

    context['public_racks'] = Rack.objects.PublicRacksForUser(user)
    context['private_racks'] = Rack.objects.OwnedRacksForUser(user)
    context['friendship_list'] = Friendship.objects.friends_for_user(user)
    context['notices'] = Notice.objects.notices_for(user)
    if request.session.has_key('fb_friends'):
        fb_friends = request.session['fb_friends']
        fb_stunable_friends = request.session['fb_stunable_friends']
        offset =random.randint(0,len(fb_friends)-20)
        context['fb_friend_list']  = fb_stunable_friends+fb_friends[offset:offset+20-len(fb_stunable_friends)]
        context['fb_token'] = request.session['fb_token']
        context['FACEBOOK_APPID'] = settings.FACEBOOK_APP_ID
    if 'cart' in request.META.get('PATH_INFO'):
        context['cart'] = Cart(request)
    return context