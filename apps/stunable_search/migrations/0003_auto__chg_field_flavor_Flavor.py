# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Flavor.Flavor'
        db.alter_column('stunable_search_flavor', 'Flavor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stunable_search.Flavor'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Flavor.Flavor'
        raise RuntimeError("Cannot reverse this migration. 'Flavor.Flavor' and its values cannot be restored.")

    models = {
        'stunable_search.flavor': {
            'Flavor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stunable_search.Flavor']", 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Flavor'},
            'Tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tagging.Tag']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'null': 'True'})
        }
    }

    complete_apps = ['stunable_search']