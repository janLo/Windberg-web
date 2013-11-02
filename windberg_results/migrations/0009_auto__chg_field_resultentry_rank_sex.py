# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ResultEntry.rank_sex'
        db.alter_column(u'windberg_results_resultentry', 'rank_sex', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'ResultEntry.rank_sex'
        db.alter_column(u'windberg_results_resultentry', 'rank_sex', self.gf('django.db.models.fields.IntegerField')(default=0))

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
            'Meta': {'ordering': "['start_time', '-creation_date']", 'object_name': 'Start'},
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'runs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Run']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'windberg_register.version': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Version'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_end': ('django.db.models.fields.DateField', [], {}),
            'starts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Start']", 'symmetrical': 'False'})
        },
        u'windberg_results.resultentry': {
            'Meta': {'ordering': "['table__id', 'rank']", 'object_name': 'ResultEntry'},
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_year': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'club': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'given': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'rank_age': ('django.db.models.fields.IntegerField', [], {}),
            'rank_sex': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'result_time': ('django.db.models.fields.TimeField', [], {}),
            'start_number': ('django.db.models.fields.IntegerField', [], {}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['windberg_results.ResultTable']"})
        },
        u'windberg_results.resulttable': {
            'Meta': {'ordering': "['version', 'start_time']", 'object_name': 'ResultTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'use_age_group': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'use_gender': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['windberg_register.Version']"})
        }
    }

    complete_apps = ['windberg_results']