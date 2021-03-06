# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Town'
        db.delete_table(u'windberg_register_town')

        # Deleting field 'Starter.town'
        db.delete_column(u'windberg_register_starter', 'town_id')

        # Deleting field 'Starter.zipno'
        db.delete_column(u'windberg_register_starter', 'zipno')

        # Deleting field 'Starter.adress'
        db.delete_column(u'windberg_register_starter', 'adress')


    def backwards(self, orm):
        # Adding model 'Town'
        db.create_table(u'windberg_register_town', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'windberg_register', ['Town'])

        # Adding field 'Starter.town'
        db.add_column(u'windberg_register_starter', 'town',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['windberg_register.Town']),
                      keep_default=False)

        # Adding field 'Starter.zipno'
        db.add_column(u'windberg_register_starter', 'zipno',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=5),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Starter.adress'
        raise RuntimeError("Cannot reverse this migration. 'Starter.adress' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Starter.adress'
        db.add_column(u'windberg_register_starter', 'adress',
                      self.gf('django.db.models.fields.CharField')(max_length=200),
                      keep_default=False)


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
        u'windberg_register.club': {
            'Meta': {'object_name': 'Club'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
        u'windberg_register.starter': {
            'Meta': {'object_name': 'Starter'},
            'birth': ('django.db.models.fields.DateField', [], {}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['windberg_register.Club']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'given': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'runs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Run']", 'symmetrical': 'False'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['windberg_register.Version']"})
        },
        u'windberg_register.version': {
            'Meta': {'object_name': 'Version'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 4, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'post_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 4, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'starts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Start']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['windberg_register']