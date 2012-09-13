from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.racks.models import Rack, Rack_Item, Item, Color, VALID_COLOR_REGEX
from apps.friends.models import Friendship


class RacksViewTest(TestCase):
    fixtures = ['data.json',]
    
    def setUp(self):
        self.user = User(username='user', email="user@sample.com", is_active=True, is_staff=True, is_superuser=True)
        self.user.set_password('user')
        self.user.save()
        login = self.client.login(username='user', password='user')
        
        # add friend ship of user with test_user1
        self.test_user1 = User(username='test_user1', email="test_user1@sample.com", is_active=True)
        self.test_user1.set_password('test_user1')
        self.test_user1.save()
        fs = Friendship(to_user = self.test_user1, from_user = self.user)
        fs.save()
        
        # add friend ship of user with test_user2
        self.test_user2 = User(username='test_user2', email="test_user2@sample.com", is_active=True)
        self.test_user2.set_password('test_user2')
        self.test_user2.save()
        fs = Friendship(to_user = self.test_user2, from_user = self.user)
        fs.save()
        
        # init data for initRack
        self.initRack = Rack(name="INIT", owner=self.user, publicity=0)
        self.initRack.save()
        self.item1 = Item(name="Item1", label='Item1Label')
        self.item1.save()
        self.item2 = Item(name="Item2", label='Item2Label')
        self.item2.save()
        self.item3 = Item(name="Item3", label='Item3Label')
        self.item3.save()
        rack_item1 = Rack_Item(item = self.item1, rack = self.initRack)
        rack_item1.save()
        rack_item2 = Rack_Item(item = self.item2, rack = self.initRack)
        rack_item2.save()
        rack_item3 = Rack_Item(item = self.item3, rack = self.initRack)
        rack_item3.save()
        
        self.initRack.shared_users.add(self.test_user1)
        self.initRack.save()
    
    def testCreateRack(self):
        response = self.client.post(reverse("racks_add"), {'name':'Private 1', 'next':reverse("racks_index")})
        self.assertRedirects(response, reverse("racks_index"))
        self.assertEquals(Rack.objects.filter(name="Private 1").count(), 1)
    
    def testAbnormalCreate(self):
        response = self.client.post(reverse("racks_add"), {'name': ''})
        self.assertContains(response, "This field is required")
        self.assertEqual(Rack.objects.filter(owner=self.user).count(), 1)
        
    def testDeleteRack(self):
        delete_rack = Rack.objects.get(name="INIT")
        response = self.client.get(reverse("rack_delete", args=[delete_rack.id, ]))
        self.assertRedirects(response, reverse("racks_index"))
        # because we have 10 default Rack in the database
        self.assertEqual(len(Rack.objects.all()), 10)    
    
    def testEdit(self):
        edit_rack = Rack.objects.get(name="INIT")
        item_list = Item.objects.all()
        item_pk_list = []
        for item in item_list:
            item_pk_list.append(item.id)
        
        shared_users = User.objects.exclude(username = "user")
        user_pk_list = []
        for user in shared_users:
            user_pk_list.append(user.id)

        response = self.client.post(reverse("rack_edit", args=[edit_rack.id, ]), {'name':'Private', 'shared_users':user_pk_list, 'rack_items': item_pk_list})       
        self.assertRedirects(response, reverse("racks_detail", args=[edit_rack.id, ]))
        self.assertEqual(Rack.objects.filter(owner=self.user).count(), 1)
        self.assertEqual(Rack.objects.filter(name="Private").count(), 1)
        self.assertEqual(len(self.initRack.shared_users.all()), 2)
        self.assertEqual(len(self.initRack.rack_items.all()), 3)
        
    def testComplexEdit(self):
        edit_rack = Rack.objects.get(name="INIT")
        item_list = Item.objects.filter(name="Item1")
        item_pk_list = []
        for item in item_list:
            item_pk_list.append(item.id)
        
        shared_users = User.objects.filter(username='test_user2')
        user_pk_list = []
        for user in shared_users:
            user_pk_list.append(user.id)

        response = self.client.post(reverse("rack_edit", args=[edit_rack.id, ]), {'name':'Private', 'shared_users':user_pk_list, 'rack_items': item_pk_list})
        self.assertRedirects(response, reverse("racks_detail", args=[edit_rack.id, ]))
        self.assertEqual(Rack.objects.filter(owner=self.user).count(), 1)
        self.assertEqual(Rack.objects.filter(name="Private").count(), 1)
        self.assertEqual(len(self.initRack.shared_users.all()), 1)
        self.assertIn(self.test_user2, self.initRack.shared_users.all())
        self.assertEqual(len(self.initRack.rack_items.all()), 1)
        self.assertIn(self.item1, self.initRack.rack_items.all())        
    
    def testDeleteItem(self):
        deletefromrack = Rack.objects.get(name="INIT")
        delete_item = Item.objects.get(name="Item1")
        response = self.client.get(reverse("rack_item_delete", args=[deletefromrack.id, delete_item.id, ]))
        self.assertRedirects(response, reverse("racks_detail", args=[deletefromrack.id]))
        self.assertEqual(len(deletefromrack.rack_items.all()), 2)
    
    def testDeleteAdmirer(self):
        deleteAdmirer = User.objects.get(username="test_user1")
        deletefromrack = Rack.objects.get(name="INIT")
        response = self.client.get(reverse("remove_admirer", args=[deletefromrack.id, deleteAdmirer.id, ]))
        self.assertRedirects(response, reverse("racks_detail", args=[deletefromrack.id, ]))
        self.assertEqual(len(deletefromrack.shared_users.all()), 0)
    
    def testAddAdmirer(self):
        addAdmirer = User.objects.get(username="test_user2")
        addtorack = Rack.objects.get(name="INIT")
        response = self.client.get(reverse("add_admirer", args=[addtorack.id, addAdmirer.id, ]))
        self.assertRedirects(response, reverse("racks_detail", args=[addtorack.id, ]))
        self.assertEqual(len(addtorack.shared_users.all()), 2)
    
    def testAbnormalAddAdmirer(self):
        addtorack = Rack.objects.get(name="INIT")
        response = self.client.get(reverse("add_admirer", args=[addtorack.id, 999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(addtorack.shared_users.all()), 1)
    
    def testAbnormalDeleteAdmirer(self):
        #deleteAdmirer = User.objects.get(pk=999)
        deletefromrack = Rack.objects.get(name="INIT")
        response = self.client.get(reverse("remove_admirer", args=[deletefromrack.id, 999, ]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(deletefromrack.shared_users.all()), 1)
        
    def testPrivateRacks(self):        
        shared_rack = Rack.objects.SharedRacksForUser(self.user)
        self.assertEqual(len(shared_rack), 1)
        for user in self.initRack.shared_users.all():
            self.initRack.shared_users.remove(user)        
        self.initRack.save()
        private_rack = Rack.objects.PrivateRacksForUser(self.user)
        shared_rack = Rack.objects.SharedRacksForUser(self.user)
        self.assertEqual(len(private_rack), 1)
        self.assertEqual(len(shared_rack), 0)
        
        #add item to default rack
        pant_rack = Rack.objects.get(name="Pants")
        pant_item = Rack_Item(item = self.item1, rack=pant_rack)
        pant_item.save()
        
        private_racks = Rack.objects.PrivateRacksForUser(self.user)
        self.assertEqual(len(private_racks), 2)
        self.assertIn(pant_rack, private_racks)
    
    def testAuthorization(self):
        self.client.logout()
        
        # login as friend of user
        login = self.client.login(username='test_user1', password='test_user1')
        response = self.client.get(reverse("racks_index"))
        private_racks = response.context['private_racks']
        self.assertEqual(len(private_racks), 0)
        response = self.client.get(reverse("list_shared_racks"))
        shared_racks = response.context['shared_racks']
        self.assertEqual(len(shared_racks), 0)
        self.assertNotContains(response, "Edit")        
        rack_share_with_you = response.context['racks_shared_with_you']
        self.assertEqual(len(rack_share_with_you), 1)
    
    def testCannotDelete(self):
        self.client.logout()
        #login as friend of user
        login = self.client.login(username='test_user1', password='test_user1')
        response = self.client.get(reverse("rack_delete", args=[self.initRack.id, ]))
        self.assertEqual(Rack.objects.filter(name="INIT").count(), 1)
        # check the Not Authorized message
    

class ColorTestCase(TestCase):
    
    def test_color_validation_regex(self):
        
        valid_colors = ['#FFFFFF', '#ffffff', '#123456', 'rgb(0,0,0)', 'rgb(10,10,10)', 'rgb(100,100,100)']
        invalid_colors = ['123456', 'rgb(1000,1000,1000)', '000']
        
        for color in valid_colors:
            self.assertRegexpMatches(color, VALID_COLOR_REGEX)
        for color in invalid_colors:
            self.assertNotRegexpMatches(color, VALID_COLOR_REGEX)
    
    def test_color_validation(self):
        # Python 2.7 only.. 
        with self.assertRaises(ValidationError):
            c = Color(name='Black', color_css="000")
            c.full_clean()
        