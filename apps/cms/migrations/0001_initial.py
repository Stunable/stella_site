# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExternalPost'
        db.create_table('cms_externalpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('post_type', self.gf('django.db.models.fields.CharField')(default='news', max_length=16)),
            ('source', self.gf('django.db.models.fields.CharField')(default='http://stunablenews.wordpress.com/', max_length=256)),
        ))
        db.send_create_signal('cms', ['ExternalPost'])


    def backwards(self, orm):
        # Deleting model 'ExternalPost'
        db.delete_table('cms_externalpost')


    models = {
        'cms.externalpost': {
            'Meta': {'object_name': 'ExternalPost'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_type': ('django.db.models.fields.CharField', [], {'default': "'news'", 'max_length': '16'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'http://stunablenews.wordpress.com/'", 'max_length': '256'}),
            'text': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cms']