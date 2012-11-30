# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteTextContent'
        db.create_table('cms_sitetextcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('html', self.gf('django.db.models.fields.TextField')(default='cms content placeholder', null=True, blank=True)),
            ('component', self.gf('django.db.models.fields.CharField')(default='All', max_length=32)),
        ))
        db.send_create_signal('cms', ['SiteTextContent'])


    def backwards(self, orm):
        # Deleting model 'SiteTextContent'
        db.delete_table('cms_sitetextcontent')


    models = {
        'cms.externalpost': {
            'Meta': {'object_name': 'ExternalPost'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'has_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_type': ('django.db.models.fields.CharField', [], {'default': "'news'", 'max_length': '16'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'http://stunablenews.wordpress.com/'", 'max_length': '256'}),
            'text': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'cms.sitetextcontent': {
            'Meta': {'object_name': 'SiteTextContent'},
            'component': ('django.db.models.fields.CharField', [], {'default': "'All'", 'max_length': '32'}),
            'html': ('django.db.models.fields.TextField', [], {'default': "'cms content placeholder'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['cms']