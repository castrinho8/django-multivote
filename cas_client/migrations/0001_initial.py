# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CasUser'
        db.create_table(u'cas_client_casuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('login', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('rawdata', self.gf('django.db.models.fields.TextField')()),
            ('doctype', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('nif', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal(u'cas_client', ['CasUser'])

        # Adding model 'CasRole'
        db.create_table(u'cas_client_casrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'cas_client', ['CasRole'])

        # Adding M2M table for field users on 'CasRole'
        m2m_table_name = db.shorten_name(u'cas_client_casrole_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('casrole', models.ForeignKey(orm[u'cas_client.casrole'], null=False)),
            ('casuser', models.ForeignKey(orm[u'cas_client.casuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['casrole_id', 'casuser_id'])


    def backwards(self, orm):
        # Deleting model 'CasUser'
        db.delete_table(u'cas_client_casuser')

        # Deleting model 'CasRole'
        db.delete_table(u'cas_client_casrole')

        # Removing M2M table for field users on 'CasRole'
        db.delete_table(db.shorten_name(u'cas_client_casrole_users'))


    models = {
        u'cas_client.casrole': {
            'Meta': {'object_name': 'CasRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cas_client.CasUser']", 'symmetrical': 'False'})
        },
        u'cas_client.casuser': {
            'Meta': {'object_name': 'CasUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'doctype': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'last_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'rawdata': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['cas_client']