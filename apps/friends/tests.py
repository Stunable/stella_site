from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from friends.models import JoinInvitation, Contact, Friendship
from apps.accounts import urls


settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

class FriendsViewTest(TestCase):
    fixtures = ['initial_data.json',]
    
    def setUp(self):
        self.user = User(username='user', email="user@sample.com", is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('user')
        self.user.save()
        login = self.client.login(username='user', password='user')
        
        self.to_user = User(username='user_friend', email="user_friend@sample.com", is_active=True, is_staff=True, is_superuser=True)
        self.to_user.set_password('user_friend')
        self.to_user.save()
        
        # add friend ship of user with test_user1
        self.test_user1 = User(username='test_user1', email="test_user1@sample.com", is_active=True)
        self.test_user1.set_password('test_user1')
        self.test_user1.save()
        fs = Friendship(to_user = self.test_user1, from_user = self.user)
        fs.save()
        
    #test simple search case
    def test_simple_search_case(self):
        # test find user
        response = self.client.get(reverse('friend_search'), {'q': 'test_user1'})
        search_result = response.context['friends_list']
        self.assertEqual(search_result.__len__(), 1)
        self.assertContains(response, 'test_user1')
    
    #test simple delete case
    def test_delete_admirer(self):
        # delete test_user1
        response = self.client.get(reverse("friend_delete", args=[self.test_user1.id]))
        #response = self.client.get('/friends/delete/' + str(self.test_user1.id))
        self.assertRedirects(response, reverse('friend_index'))
        response = self.client.get(reverse('friend_index'))
        user_friends = response.context['friends_list']
        self.assertEqual(len(user_friends), 0)
        
        # test if friendship is delete between two users
        self.assertEqual(Friendship.objects.filter(from_user=self.user,to_user=self.to_user).count(), 0)    
    
    def test_invite_join(self):
        """
        Invite new user to join test case
        
        """
        response = self.client.post(reverse('friend_invite'), {'emails': 'friend1@sample.com, friend2@sample.com', 'email_message':'invite message'})
        
        c = Contact.objects.get(email='friend1@sample.com')
        join_invitation = JoinInvitation.objects.get(contact = c)
        #url = '/friends/accept_join/' + join_invitation.confirmation_key
        response = self.client.get(reverse('friend_accept_join', args=[join_invitation.confirmation_key, ]))
        self.assertRedirects(response, reverse(urls.profile_edit))
        
        # if user has join the website
        self.assertEqual(User.objects.filter(username=self.user.username).count(), 1)
        
        # test the number of users after new user has joined
        self.assertEqual(len(User.objects.all()), 4)
        
        # test list of users
        self.client.logout()
        self.client.login(username='user', password='user')        
        response = self.client.get(reverse('friend_index'))
        user_friends = response.context['friends_list']
        self.assertEqual(len(user_friends), 2)
        
        # test if test_user1 and new_user is in user's admirers 
        self.assertContains(response, 'test_user1')
        self.assertContains(response, 'friend1@sample.com')
        
        # test delete new user
        new_user = User.objects.get(email = 'friend1@sample.com')
        response = self.client.get(reverse('friend_delete', args=[new_user.id, ]))
        self.assertRedirects(response, reverse('friend_index'))
        response = self.client.get(reverse('friend_index'))
        user_friends = response.context['friends_list']
        self.assertEqual(len(user_friends), 1)
        # test if friendship is delete between two users
        self.assertEqual(Friendship.objects.filter(from_user=self.user,to_user=self.to_user).count(), 0)

    # test accept case of invite_friend        
    def test_invite_friend_accept(self):
        response = self.client.post(reverse('friend_invite'), {'emails': 'user_friend@sample.com', 'email_message':'invite message'})
        
        self.client.logout()
        
        # login as friend of user
        login = self.client.login(username='user_friend', password='user_friend')
        
        # test to see notification
        response = self.client.get(reverse('notification_notices'))
        
        # check to see these is invite friend notice
        notices = response.context['notices']
        
        self.assertIsNotNone(notices)
        
        self.assertEqual(notices[0].recipient, self.to_user)
        self.assertEqual(notices[0].sender, self.user)
        
        # test the number of notifications before clicking the accept button
        self.assertEqual(len(notices), 1)
    
        self.client.get(reverse('accept_invitation', args=[self.user.username, notices[0].id]))
        
        # test the number of notification after clicking the Accept button
        response = self.client.get(reverse('notification_notices'))
        notices = response.context['notices']
        self.assertEqual(len(notices), 2)
        
        # friendship should be created between users
        self.assertEqual(Friendship.objects.filter(from_user=self.user,to_user=self.to_user).count(), 1)
        
        # test search for friends of user
        self.client.logout()
        self.client.login(username='user', password='user')
        response = self.client.get(reverse('friend_search'), {'q': 'user'})
        search_result = response.context['friends_list']
        self.assertEqual(len(search_result), 2)
        self.assertContains(response, 'test_user1')
        self.assertContains(response, 'user_friend')
        
        # test delete test_user1
        response = self.client.get(reverse('friend_delete', args=[self.test_user1.id, ]))
        self.assertRedirects(response, reverse('friend_index'))
        response = self.client.get(reverse('friend_index'))
        user_friends = response.context['friends_list']
        self.assertEqual(len(user_friends), 1)
        
        # test if friendship is delete between two users
        self.assertEqual(Friendship.objects.filter(from_user=self.user,to_user=self.test_user1).count(), 0)
        
        # test search for friends of user
        response = self.client.get(reverse('friend_search'), {'q': 'user'})
        search_result = response.context['friends_list']
        self.assertEqual(len(search_result), 1)
        self.assertContains(response, 'user_friend')
    
    # test deline case of invite friend    
    def test_invite_friend_decline(self):
        response = self.client.post(reverse('friend_invite'), {'emails': 'user_friend@sample.com', 'email_message':'invite message'})
        
        self.client.logout()
        
        # login as friend of user
        login = self.client.login(username='user_friend', password='user_friend')
        
        # test to see notification
        response = self.client.get(reverse('notification_notices'))
        
        # check to see these is invite friend notice
        notices = response.context['notices']
        
        self.assertIsNotNone(notices)
        
        self.assertEqual(notices[0].recipient, self.to_user)
        self.assertEqual(notices[0].sender, self.user)
        
        # test the number of notifications before clicking the accept button
        self.assertEqual(len(notices), 1)
    
        self.client.get(reverse('decline_invitation', args=[self.user.username, notices[0].id]))
        
        # test the number of notification after clicking the Accept button
        response = self.client.get(reverse('notification_notices'))
        notices = response.context['notices']
        self.assertEqual(len(notices), 1)
        
        # friendship should not be created between users
        self.assertEqual(Friendship.objects.filter(from_user=self.user,to_user=self.to_user).count(), 0)
    
        