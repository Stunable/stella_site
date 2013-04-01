from racks.models import Rack
from friends.models import Friendship
from notification.models import Notice
from kart.models import Cart
import random
from django.conf import settings

def racks(request):
    context = {'URL':settings.WWW_ROOT,'STATIC_URL':settings.STATIC_URL}
    if not settings.DEBUG:
        context['SECURE_ROOT'] = settings.WWW_ROOT.rstrip('/')
    context['FACEBOOK_APPID'] = settings.FACEBOOK_APP_ID
    user = request.user
    
    
    # context['friendship_list'] = Friendship.objects.friends_for_user(user)
    # context['notices'] = Notice.objects.notices_for(user)
    # if request.session.has_key('fb_friends'):
    #     fb_friends = request.session['fb_friends']
    #     fb_stunable_friends = request.session['fb_stunable_friends']
    #     if len(fb_friends) > 20:
    #         offset =random.randint(0,len(fb_friends)-20)
    #         context['fb_friend_list']  = fb_stunable_friends+fb_friends[offset:offset+20-len(fb_stunable_friends)]
    #     else:
    #         context['fb_friend_list'] = fb_stunable_friends+fb_friends
    #     context['fb_token'] = request.session['fb_token']
    # if 'cart' in request.META.get('PATH_INFO'):
    context['cart'] = Cart(request)
    return context