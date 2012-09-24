# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ExternalPost.has_content'
        db.add_column('cms_externalpost', 'has_content',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ExternalPost.has_content'
        db.delete_column('cms_externalpost', 'has_content')


    models = {
        'cms.externalpost': {
            'Meta': {'object_name': 'ExternalPost'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'has_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_type': ('django.db.models.fields.CharField', [], {'default': "'news'", 'max_length': '16'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'http://stunablenews.wordpress.com/'", 'max_length': '256'}),
            'text': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cms']