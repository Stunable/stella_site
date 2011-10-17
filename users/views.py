# Create your views here.
"""Views for the users. Responses for various account related requests.
"""

from django.template import Context, loader
from users.models import StellaUser
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    """Static page for users to sign in to. 
    """
    return render_to_response('login.html')
