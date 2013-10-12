# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AgeGroup'
        db.create_table(u'windberg_register_agegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('min_age', self.gf('django.db.models.fields.IntegerField')()),
            ('max_age', self.gf('django.db.models.fields.IntegerField')()),
            ('is_pseudo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_detail', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'windberg_register', ['AgeGroup'])

        # Adding model 'Run'
        db.create_table(u'windberg_register_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('distance', self.gf('django.db.models.fields.IntegerField')()),
            ('has_ages', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'windberg_register', ['Run'])

        # Adding M2M table for field possible_ages on 'Run'
        m2m_table_name = db.shorten_name(u'windberg_register_run_possible_ages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('run', models.ForeignKey(orm[u'windberg_register.run'], null=False)),
            ('agegroup', models.ForeignKey(orm[u'windberg_register.agegroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['run_id', 'agegroup_id'])

        # Adding model 'Start'
        db.create_table(u'windberg_register_start', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'windberg_register', ['Start'])

        # Adding M2M table for field runs on 'Start'
        m2m_table_name = db.shorten_name(u'windberg_register_start_runs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('start', models.ForeignKey(orm[u'windberg_register.start'], null=False)),
            ('run', models.ForeignKey(orm[u'windberg_register.run'], null=False))
        ))
        db.create_unique(m2m_table_name, ['start_id', 'run_id'])

        # Adding model 'Version'
        db.create_table(u'windberg_register_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('post_end', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 9, 17, 0, 0), auto_now=True, blank=True)),
            ('net_end', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 9, 17, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'windberg_register', ['Version'])

        # Adding M2M table for field starts on 'Version'
        m2m_table_name = db.shorten_name(u'windberg_register_version_starts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('version', models.ForeignKey(orm[u'windberg_register.version'], null=False)),
            ('start', models.ForeignKey(orm[u'windberg_register.start'], null=False))
        ))
        db.create_unique(m2m_table_name, ['version_id', 'start_id'])

        # Adding model 'Town'
        db.create_table(u'windberg_register_town', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'windberg_register', ['Town'])

        # Adding model 'Club'
        db.create_table(u'windberg_register_club', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'windberg_register', ['Club'])

        # Adding model 'Starter'
        db.create_table(u'windberg_register_starter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('given', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('birth', self.gf('django.db.models.fields.DateField')()),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['windberg_register.Club'])),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('adress', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['windberg_register.Town'])),
            ('zipno', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['windberg_register.Version'])),
        ))
        db.send_create_signal(u'windberg_register', ['Starter'])

        # Adding M2M table for field runs on 'Starter'
        m2m_table_name = db.shorten_name(u'windberg_register_starter_runs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('starter', models.ForeignKey(orm[u'windberg_register.starter'], null=False)),
            ('run', models.ForeignKey(orm[u'windberg_register.run'], null=False))
        ))
        db.create_unique(m2m_table_name, ['starter_id', 'run_id'])


    def backwards(self, orm):
        # Deleting model 'AgeGroup'
        db.delete_table(u'windberg_register_agegroup')

        # Deleting model 'Run'
        db.delete_table(u'windberg_register_run')

        # Removing M2M table for field possible_ages on 'Run'
        db.delete_table(db.shorten_name(u'windberg_register_run_possible_ages'))

        # Deleting model 'Start'
        db.delete_table(u'windberg_register_start')

        # Removing M2M table for field runs on 'Start'
        db.delete_table(db.shorten_name(u'windberg_register_start_runs'))

        # Deleting model 'Version'
        db.delete_table(u'windberg_register_version')

        # Removing M2M table for field starts on 'Version'
        db.delete_table(db.shorten_name(u'windberg_register_version_starts'))

        # Deleting model 'Town'
        db.delete_table(u'windberg_register_town')

        # Deleting model 'Club'
        db.delete_table(u'windberg_register_club')

        # Deleting model 'Starter'
        db.delete_table(u'windberg_register_starter')

        # Removing M2M table for field runs on 'Starter'
        db.delete_table(db.shorten_name(u'windberg_register_starter_runs'))


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
            'Meta': {'object_name': 'Run'},
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
            'adress': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'birth': ('django.db.models.fields.DateField', [], {}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['windberg_register.Club']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'given': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'runs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Run']", 'symmetrical': 'False'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['windberg_register.Town']"}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['windberg_register.Version']"}),
            'zipno': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'windberg_register.town': {
            'Meta': {'object_name': 'Town'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'windberg_register.version': {
            'Meta': {'object_name': 'Version'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'net_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 17, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'post_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 17, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'starts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['windberg_register.Start']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['windberg_register']