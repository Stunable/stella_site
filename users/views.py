# Create your views here.
"""Views for the users. Responses for various account related requests.
"""

from django.template import Context, loader
from users.models import StellaUser
from django.http import HttpResponse

def index(request):
    """Static page for users to sign in to. 
    """
    t = loader.get_template('templates/main.html')
    return HttpResponse(t.render())
