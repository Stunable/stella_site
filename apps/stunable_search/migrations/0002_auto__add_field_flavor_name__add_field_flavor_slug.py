# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Flavor.name'
        db.add_column('stunable_search_flavor', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Adding field 'Flavor.slug'
        db.add_column('stunable_search_flavor', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Flavor.name'
        db.delete_column('stunable_search_flavor', 'name')

        # Deleting field 'Flavor.slug'
        db.delete_column('stunable_search_flavor', 'slug')


    models = {
        'stunable_search.flavor': {
            'Flavor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stunable_search.Flavor']"}),
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