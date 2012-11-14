from racks.models import Rack
from friends.models import Friendship
from notification.models import Notice
from cart.cart import Cart


def racks(request):
    context = {}
    user = request.user
    
    if user.is_authenticated():
        context['public_racks'] = Rack.objects.PublicRacksForUser(user)
        context['private_racks'] = Rack.objects.PrivateRacksForUser(user)
        context['friendship_list'] = Friendship.objects.friends_for_user(user)
        context['notices'] = Notice.objects.notices_for(user)
        if 'cart' in request.META.get('PATH_INFO'):
            context['cart'] = Cart(request)
    return context