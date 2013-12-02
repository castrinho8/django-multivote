# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CasRole.grants_permissions'
        db.add_column(u'cas_client_casrole', 'grants_permissions',
                      self.gf('django.db.models.fields.TextField')(default='[]'),
                      keep_default=False)

        # Adding field 'CasRole.revoke_permissions'
        db.add_column(u'cas_client_casrole', 'revoke_permissions',
                      self.gf('django.db.models.fields.TextField')(default='[]'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CasRole.grants_permissions'
        db.delete_column(u'cas_client_casrole', 'grants_permissions')

        # Deleting field 'CasRole.revoke_permissions'
        db.delete_column(u'cas_client_casrole', 'revoke_permissions')


    models = {
        u'cas_client.casrole': {
            'Meta': {'object_name': 'CasRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'grants_permissions': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'revoke_permissions': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
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