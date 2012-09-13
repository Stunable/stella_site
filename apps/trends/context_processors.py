from notification.models import Notice

def trend_count(request):
    # Pretty hacky duplicate of notification.context_processors, just to get a count of a specific
    # Notice type. Would be much better to add this functionality to notifications app (and as a
    # template tag instead of a context processor)
    if request.user.is_authenticated():
        return {
            'trends_unseen_count': Notice.objects.notices_for(request.user, on_site=True, unseen=True).filter(notice_type__label='share_item').count()
        }
    return {}