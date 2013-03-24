from StringIO import StringIO
from PIL import Image
import urllib2    

import json



def add_fb_friends_to_list(list, js):
    if js.get('paging'):
        if js.get('paging').get('next'):
            req = urllib2.Request(url=js['paging']['next'])
            content = urllib2.urlopen(req)
            js = json.load(content)
            for x in xrange(0, len(js['data'])):
                list.append(js['data'][x])
            add_fb_friends_to_list(list, js)



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
   

def get_google_avatar_image(social_user):
    access_token = social_user.tokens['access_token']
    url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + access_token
    req = urllib2.Request(url=url)
    content = urllib2.urlopen(req)
    d = json.loads(content.read())

    print d

    if d.has_key('picture'):

        url = d['picture']+'?access_token=' + access_token

        print url

        req = urllib2.Request(url=url)
        content = urllib2.urlopen(req)
        # print StringIO(content.read())
        # print content.read()
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

