# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CheckList'
        db.create_table('checkApp_checklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('checkApp', ['CheckList'])

    def backwards(self, orm):

        # Deleting model 'CheckList'
        db.delete_table('checkApp_checklist')

    models = {
        'checkApp.checklist': {
            'Meta': {'object_name': 'CheckList'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['checkApp']
