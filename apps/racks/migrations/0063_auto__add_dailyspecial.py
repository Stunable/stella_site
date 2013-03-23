# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DailySpecial'
        db.create_table('racks_dailyspecial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128, null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('weekday', self.gf('apps.weekday_field.fields.WeekdayField')(max_length=14, null=True, blank=True)),
        ))
        db.send_create_signal('racks', ['DailySpecial'])

        # Adding M2M table for field Items on 'DailySpecial'
        db.create_table('racks_dailyspecial_Items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dailyspecial', models.ForeignKey(orm['racks.dailyspecial'], null=False)),
            ('item', models.ForeignKey(orm['racks.item'], null=False))
        ))
        db.create_unique('racks_dailyspecial_Items', ['dailyspecial_id', 'item_id'])


    def backwards(self, orm):
        # Deleting model 'DailySpecial'
        db.delete_table('racks_dailyspecial')

        # Removing M2M table for field Items on 'DailySpecial'
        db.delete_table('racks_dailyspecial_Items')


    models = {
        'accounts.anonymousprofile': {
            'Meta': {'object_name': 'AnonymousProfile'},
            'favourite_designer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_login': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'racks.brand': {
            'Meta': {'object_name': 'Brand'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.PriceCategory']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
        'racks.dailyspecial': {
            'Items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['racks.Item']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'DailySpecial'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'weekday': ('apps.weekday_field.fields.WeekdayField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'})
        },
        'racks.denimcolormanager': {
            'Meta': {'object_name': 'DenimColorManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'racks.plaincolormanager': {
            'Meta': {'object_name': 'PlainColorManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'racks.pricecategory': {
            'Meta': {'object_name': 'PriceCategory'},
            'display_value': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
        'racks.rack': {
            'Meta': {'object_name': 'Rack'},
            'anon_user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.AnonymousProfile']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publicity': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rack_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['racks.Item']", 'through': "orm['racks.Rack_Item']", 'symmetrical': 'False'}),
            'shared_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'shared_users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_by_user'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'racks.rack_item': {
            'Meta': {'object_name': 'Rack_Item'},
            'created_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.Item']"}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['racks.Rack']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['racks']