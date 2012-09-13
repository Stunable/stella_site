"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User

# monkeypatch debug-toolbar so it doesn't intercept redirects
from debug_toolbar.middleware import DebugToolbarMiddleware
def process_response(self, request, response):
    return response
DebugToolbarMiddleware.process_response = process_response


TEST_USER_NAME = 'test_user'
TEST_USER_PASSWORD = '12345'

class TestRedirects(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username=TEST_USER_NAME)
        self.user.set_password(TEST_USER_PASSWORD)
        self.user.save()
    
    def test_redirect_unauth_user_to_login(self):
        resp = self.client.get("/", follow=True)
        self.assertEquals([('http://testserver/racks/carousel/all', 302),
                           ('http://testserver/accounts/login/?next=/racks/carousel/all', 302)],
                           resp.redirect_chain)
    
    def test_redirect_auth_user_to_carousel(self):
        self.client.login(username=TEST_USER_NAME, password=TEST_USER_PASSWORD)
        resp = self.client.get("/", follow=True)
        self.assertEquals([('http://testserver/racks/carousel/all', 302),
                           ('http://testserver/accounts/welcome', 302)],
                           resp.redirect_chain)
