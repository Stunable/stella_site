from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import notification.models as notification


def trend_notice_modal(request):
    """
    Returns a list of 'share_item' or 'share_item_sent' notifications.
    """
    
    # rendered notices being stored in the DB make styling the templates a pain. This little
    # gem will create shiny new ones every time you open the modal : )
    # to use, add ?debug=1 to the url to the trend_notice_modal view (in user_base.html)
    
    # comment out in case of re-use
#    if request.GET.get('debug', False):
#        from django.conf import settings
#        if settings.DEBUG:
#            notification.Notice.objects.all().delete()
#            from apps.racks.models import Item
#            from django.contrib.auth.models import User
#            item = Item.objects.all()[10]
#            from_user = User.objects.get(id=2)
#            for i in range(0,3):
#                notification.send([request.user], 'share_item', {'item':item, 'text': 'Check this out!'}, True, from_user)
#                notification.send([from_user], 'share_item_sent', {'item':item, 'text': 'Check this out!'}, True, request.user)
#        
#    notices = notification.Notice.objects.notices_for(request.user, on_site=True).filter(notice_type__label='share_item')
#    print "Retrieved ", len(notices), " notices"
#    context = {'notices': notices}
#    return render_to_response("trends/modal.html", context,
#                              context_instance=RequestContext(request))
#    notices = notification.Notice.objects.notices_for(request.user).filter(unseen=True, notice_type__label='share_item')
    notices = notification.Notice.objects.notices_for(request.user).filter(notice_type__label='share_item')
    context = {'notices': notices}
    return render_to_response("trends/modal.html", context, context_instance=RequestContext(request))


def delete_notice(request, notice_id):
    """
    Deletes a notice
    """
    if request.method == "POST":
        notice = get_object_or_404(notification.Notice, id=notice_id)
        if notice.recipient != request.user:
            return HttpResponseForbidden()
        notice.delete()
        if request.is_ajax():
            return HttpResponse();
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    return HttpResponseNotAllowed(['POST']);
