# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


# these could be taken out of retailers to be made more generic
from apps.retailers.models import PortableConnection,ShopifyConnection

from django.contrib.auth import login




def get_api(api):
	# shopify has its own thing...
	return {
		'portable':PortableConnection

	}[api]()

def hookup(request,API=None):

	connection,retailer_profile = get_api(API).get_or_create_from_request(request)

	if connection:
		request.session['active_api_connection'] = connection
		request.session['active_retailer_profile'] = retailer_profile

	if retailer_profile.user:
		user = retailer_profile.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)



		return redirect(reverse('product_list'))
	else:	
		return redirect(reverse('create_retailer_profile'))