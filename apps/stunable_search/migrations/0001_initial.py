# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Flavor'
        db.create_table('stunable_search_flavor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Flavor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stunable_search.Flavor'])),
        ))
        db.send_create_signal('stunable_search', ['Flavor'])

        # Adding M2M table for field Tags on 'Flavor'
        db.create_table('stunable_search_flavor_Tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flavor', models.ForeignKey(orm['stunable_search.flavor'], null=False)),
            ('tag', models.ForeignKey(orm['tagging.tag'], null=False))
        ))
        db.create_unique('stunable_search_flavor_Tags', ['flavor_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Flavor'
        db.delete_table('stunable_search_flavor')

        # Removing M2M table for field Tags on 'Flavor'
        db.delete_table('stunable_search_flavor_Tags')


    models = {
        'stunable_search.flavor': {
            'Flavor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stunable_search.Flavor']"}),
            'Meta': {'object_name': 'Flavor'},
            'Tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tagging.Tag']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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