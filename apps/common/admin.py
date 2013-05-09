from django.contrib import admin 

class NotificationSender(object):

    def send_notifications(self,request,queryset):
        for o in queryset:
            o.send_notifications()
 