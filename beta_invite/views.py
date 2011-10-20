"""
Views for signing up to beta. 
"""

from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm

from beta_invite.forms import SignupForm
from beta_invite.models import SignupProfile


def signup(request, success_url='static/thankyou.html'):
    """
    Creates a new BetaUser that only has an email address and registration key. Once they are
    deemed ready to join the Beta, they can be emailed a link to register unique to them. 
    """
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_beta_user = form.save(profile_callback=profile_callback)
            return HttpResponseRedirect(success_url)
        
    else:
        # Need to add the form elements for login
        render_to_response('registration/login.html',
                           { 'form': AuthenticationForm()})
