# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'CheckItem'
        db.create_table('checkApp_checkitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('checkList', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['checkApp.CheckList'])),
        ))
        db.send_create_signal('checkApp', ['CheckItem'])

    def backwards(self, orm):

        # Deleting model 'CheckItem'
        db.delete_table('checkApp_checkitem')

    models = {
        'checkApp.checkitem': {
            'Meta': {'object_name': 'CheckItem'},
            'checkList': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['checkApp.CheckList']"}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'checkApp.checklist': {
            'Meta': {'object_name': 'CheckList'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['checkApp']
