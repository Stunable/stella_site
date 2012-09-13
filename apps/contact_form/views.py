from django.core.context_processors import csrf
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.forms.models import modelformset_factory
from contact_form.models import Contact

from django.conf import settings
from django.http import HttpResponse
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.contrib.sites.models import Site
import json
from contact_form.forms import ContactForm

def contact(request):
    c = {}
    c.update(csrf(request))
    c['menu'] = 5

    contactFormSet = modelformset_factory(Contact)

    if request.method == 'POST':
        contact = ContactForm(request.POST)
        if contact.is_valid():
           contact = contact.save()
           
           current_site = Site.objects.get_current()
        
           subject = render_to_string('contact_form/msg_subject.txt',
                                      { 'site': current_site })
           # Email subject *must not* contain newlines
           subject = ''.join(subject.splitlines())
        
           message = render_to_string('contact_form/msg.txt',
                                     {'contact': contact.firstname + ' ' + contact.lastname,
                                      'email': contact.email,
                                      'message': contact.message,
                                      'site': current_site })
             
           send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [mail_tuple[1] for mail_tuple in settings.CONTACT_LIST])
           
           # send mail to contact person to inform them the email has been sent
           reply_subject = render_to_string('contact_form/reply_subject.txt', {})
           reply_message = render_to_string('contact_form/reply_message.txt',
                                            {'firstname': contact.firstname})
           send_mail(reply_subject, reply_message, settings.DEFAULT_FROM_EMAIL, [contact.email])
           
           if request.is_ajax():
                return HttpResponse(json.dumps({'success': True}), mimetype='application/json')
           else:
                return render(request,'contact_form/message_sent.html')
        
        else:
           return HttpResponse(json.dumps({'success': False, 'errors': contact.errors}), mimetype='application/json')
           for error in contact.errors:
               messages.add_message(request,messages.ERROR,error)
    else: 
        storage = messages.get_messages(request)
        storage.used = False
        c['contact'] = ContactForm()

    return render(request,"contact_form/stella_contact.html", c)
