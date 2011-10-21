"""
Unit tests for beta_invite.

"""

from django.test import TestCase
from django.core import mail

from beta_invite.models import BetaInviteProfile

class InvitationTestCase(TestCase):
    """
    Tests that the invitation mechanism works in general.
    """
    def setUp(self):
        self.beta_valid = BetaInviteProfile.objects.create_invite_profile(email="foo@bar.com")

    def test_invitation_profile_created(self):
        """
        Test that a BetaInviteProfile was created.
        """
        self.assertEqual(BetaInviteProfile.objects.count(), 1)

    def test_thank_you_email(self):
        """
        Tests that a thank you email was sent to the email address for which
        an invitation was requested. 
        """
        self.assertEqual(len(mail.outbox), 1)
        
    def test_invitation_email(self):
        """
        Tests that an invitation email was sent with the registration link.
        """
        self.beta_valid.invite()
        self.assertEqual(len(mail.outbox), 2)
        self.assertTrue(self.beta_valid.invited)
        
    def test_register_invite(self):
        """
        Tests that this user is actually allowed to register since they have not done so yet. 
        """
        self.assertTrue(BetaInviteProfile.objects.register_invite(self.beta_valid.activation_key))

    def test_finalize_invite(self):
        """
        Tests that the profile has an invalid activation key after finalizing a registration.
        """
        self.assertTrue(BetaInviteProfile.objects.finalize_invite(self.beta_valid.activation_key))
        self.assertFalse(BetaInviteProfile.objects.register_invite(self.beta_valid.activation_key))
        
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
