# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResultTable'
        db.create_table(u'windberg_results_resulttable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['windberg_register.Version'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'windberg_results', ['ResultTable'])

        # Adding model 'ResultEntry'
        db.create_table(u'windberg_results_resultentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('given', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('birth_year', self.gf('django.db.models.fields.DateField')()),
            ('age_group', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('club', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('rank_age', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'windberg_results', ['ResultEntry'])


    def backwards(self, orm):
        # Deleting model 'ResultTable'
        db.delete_table(u'windberg_results_resulttable')

        # Deleting model 'ResultEntry'
        db.delete_table(u'windberg_results_resultentry')


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
            'Meta': {'object_name': 'ResultEntry'},
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_year': ('django.db.models.fields.DateField', [], {}),
            'club': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'given': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'rank_age': ('django.db.models.fields.IntegerField', [], {})
        },
        u'windberg_results.resulttable': {
            'Meta': {'object_name': 'ResultTable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['windberg_register.Version']"})
        }
    }

    complete_apps = ['windberg_results']