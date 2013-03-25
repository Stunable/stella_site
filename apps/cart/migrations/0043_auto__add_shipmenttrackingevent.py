# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShipmentTrackingEvent'
        db.create_table('cart_shipmenttrackingevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('shipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Shipment'])),
        ))
        db.send_create_signal('cart', ['ShipmentTrackingEvent'])


    def backwards(self, orm):
        # Deleting model 'ShipmentTrackingEvent'
        db.delete_table('cart_shipmenttrackingevent')


    models = {
        'accounts.address': {
            'Meta': {'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '250'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'addresses'", 'null': 'True', 'to': "orm['accounts.UserProfile']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'accounts.shippinginfo': {
            'Meta': {'object_name': 'ShippingInfo', '_ormbases': ['accounts.Address']},
            'address_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Address']", 'unique': 'True', 'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'age_range': ('django.db.models.fields.CharField', [], {'default': "'optional'", 'max_length': '30'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'default_cc': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'favourite_designer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_login': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'view_happenings': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'cart.cart': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Cart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'destination_zip_code': ('django.db.models.fields.CharField', [], {'default': "'60606'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'grand_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'shipping_and_handling_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'shipping_method': ('django.db.models.fields.related.ForeignKey', [], {'default': '4', 'to': "orm['retailers.ShippingType']", 'null': 'True', 'blank': 'True'})
        },
        'cart.checkout': {
            'Meta': {'object_name': 'Checkout'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kart.Kart']"}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'purchaser_checkout_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'retailer_checkout_set'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'cart.item': {
            'Meta': {'ordering': "('cart',)", 'object_name': 'Item'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Cart']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.RetailerProfile']"}),
            'sales_tax_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '18', 'decimal_places': '2', 'blank': 'True'}),
            'shipping_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '18', 'decimal_places': '2', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ordered'", 'max_length': '250'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'})
        },
        'cart.purchase': {
            'Meta': {'object_name': 'Purchase'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kart.Kart']"}),
            'checkout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Checkout']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kart.KartItem']"}),
            'purchased_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'reason_for_return': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.ShippingInfo']", 'null': 'True', 'blank': 'True'}),
            'shipping_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.ShippingType']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'placed'", 'max_length': '32'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stunable_wepay.WePayTransaction']"})
        },
        'cart.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'delivery_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'originator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'purchases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cart.Purchase']", 'symmetrical': 'False', 'blank': 'True'}),
            'ship_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'cart.shipmenttrackingevent': {
            'Meta': {'object_name': 'ShipmentTrackingEvent'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cart.Shipment']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kart.kart': {
            'Meta': {'object_name': 'Kart'},
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 25, 0, 0)'}),
            'grand_total': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_total': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'total_fees': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'total_items': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_shipping': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'total_tax': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'kart.kartitem': {
            'Meta': {'object_name': 'KartItem'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'item_variation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.ItemType']"}),
            'kart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kart.Kart']"}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.RetailerProfile']"}),
            'shipping_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.ShippingType']", 'null': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'})
        },
        'racks.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True'})
        },
        'racks.color': {
            'Meta': {'object_name': 'Color'},
            'color_css': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_denim': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'swatch': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'racks.item': {
            'Meta': {'object_name': 'Item'},
            '_retailer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'retailer_item_set'", 'null': 'True', 'to': "orm['retailers.RetailerProfile']"}),
            'api_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'item_api_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'approved': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.Category']", 'null': 'True', 'blank': 'True'}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['racks.Color']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fabrics': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'featured_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'item_featured_image_set'", 'null': 'True', 'to': "orm['racks.ProductImage']"}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_urls': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_onsale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'price_text': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'retailers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'through': "orm['retailers.StylistItem']", 'blank': 'True'}),
            'sizes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['racks.Size']", 'null': 'True', 'through': "orm['racks.ItemType']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'upload': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.ProductUpload']", 'null': 'True', 'blank': 'True'})
        },
        'racks.itemtype': {
            'Meta': {'unique_together': "(('item', 'size', 'custom_color_name'),)", 'object_name': 'ItemType'},
            'SKU': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'api_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variation_api_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'custom_color_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.ProductImage']", 'null': 'True', 'blank': 'True'}),
            'inventory': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'is_onsale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'types'", 'to': "orm['racks.Item']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['racks.Size']"})
        },
        'racks.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'bg_color': ('django.db.models.fields.CharField', [], {'default': "'white'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'extralarge': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'item_image_set'", 'null': 'True', 'to': "orm['racks.Item']"}),
            'large': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pretty_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tiny': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'racks.size': {
            'Meta': {'object_name': 'Size'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'retailers.productupload': {
            'Meta': {'object_name': 'ProductUpload'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.RetailerProfile']"}),
            'uploaded_zip': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'retailers.retailerprofile': {
            'Meta': {'object_name': 'RetailerProfile'},
            'accept_refund': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'company_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'hours': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'more_details': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'not_accept_refund': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'selling_options': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'shipping_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['retailers.ShippingType']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'welcome_message_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wepay_acct': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'wepay_token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'retailers.shippingtype': {
            'Meta': {'object_name': 'ShippingType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_arrival_time': ('django.db.models.fields.CharField', [], {'default': "'3-5 days'", 'max_length': '200'}),
            'estimated_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price_description': ('django.db.models.fields.CharField', [], {'default': "'Free Today Only!'", 'max_length': '200'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'vendor_tag': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'retailers.stylistitem': {
            'Meta': {'object_name': 'StylistItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.Item']"}),
            'stylist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'stunable_wepay.wepaytransaction': {
            'Meta': {'object_name': 'WePayTransaction'},
            'checkout_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 25, 0, 0)'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailers.RetailerProfile']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['cart']