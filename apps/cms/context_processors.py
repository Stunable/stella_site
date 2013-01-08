from django.db.models import Q
from models import *
#this just handles the 

def CMS(request):
    out = {}
    cms_entries = SiteTextContent.objects.filter(component='all')
    sp = request.path_info.split('/')
    if len(sp)>1:
        component = sp[1]
        cms_entries = SiteTextContent.objects.filter(Q(component='all') | Q(component=component))

    for e in cms_entries:
        out[e.item_name] = e.html
        if e.html == 'cms content placeholder':
            out[e.item_name] = e.html+ ':<a href="/admin/CMS/sitetextcontent/'+str(e.id)+'/">'+e.item_name+'</a>'
    
    return {'CMS':out}