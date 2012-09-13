from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^$',
        'contact_form.views.contact',name='main-contact'),
)
