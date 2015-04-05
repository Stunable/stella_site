from django.shortcuts import render, get_object_or_404, redirect

from django.http import Http404

from models import *



def text_test(request):
    template = "test.html"
    if request.user.is_staff:
        ctx = {'list': SiteTextContent.objects.all().order_by('item_name')}
        return render(request, template, ctx)
    else:
        raise Http404