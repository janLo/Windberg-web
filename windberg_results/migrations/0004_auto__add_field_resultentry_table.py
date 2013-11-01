# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ResultEntry.table'
        db.add_column(u'windberg_results_resultentry', 'table',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['windberg_results.ResultTable']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ResultEntry.table'
        db.delete_column(u'windberg_results_resultentry', 'table_id')


    models = {
        u'windberg_register.agegroup': {
            'Meta': {'object_name': 'AgeGroup'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_detail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_pseudo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {}),
            'min_age': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'windberg_register.run': {
            'Meta': {'ordering': "['distance']", 'object_name': 'Run'},
            'distance': ('django.db.models.fields.IntegerField', [], {}),
            'has_ages': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'possible_ages': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.AgeGroup']", 'symmetrical': 'False'})
        },
        u'windberg_register.start': {
            'Meta': {'object_name': 'Start'},
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'runs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Run']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'windberg_register.version': {
            'Meta': {'object_name': 'Version'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_end': ('django.db.models.fields.DateField', [], {}),
            'starts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Start']", 'symmetrical': 'False'})
        },
        u'windberg_results.resultentry': {
            'Meta': {'ordering': "['table__id', 'rank']", 'object_name': 'ResultEntry'},
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_year': ('django.db.models.fields.DateField', [], {}),
            'club': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'given': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'rank_age': ('django.db.models.fields.IntegerField', [], {}),
            'result_time': ('django.db.models.fields.TimeField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['windberg_results.ResultTable']"})
        },
        u'windberg_results.resulttable': {
            'Meta': {'object_name': 'ResultTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['windberg_register.Version']"})
        }
    }

    complete_apps = ['windberg_results']
