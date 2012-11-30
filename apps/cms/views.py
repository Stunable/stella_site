from django.views.generic.simple import direct_to_template
from django.http import Http404

from models import *



def text_test(request):
    template = "test.html"
    if request.user.is_staff:
        ctx = {'list': SiteTextContent.objects.all().order_by('item_name')}
        return direct_to_template(request, template, ctx)
    else:
        raise Http404