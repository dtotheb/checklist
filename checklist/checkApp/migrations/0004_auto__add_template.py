# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Template'
        db.create_table('checkApp_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pickledTasks', self.gf('picklefield.fields.PickledObjectField')(null=True)),
        ))
        db.send_create_signal('checkApp', ['Template'])


    def backwards(self, orm):
        
        # Deleting model 'Template'
        db.delete_table('checkApp_template')


    models = {
        'checkApp.checklist': {
            'Meta': {'object_name': 'CheckList'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'checkApp.task': {
            'Meta': {'object_name': 'Task'},
            'checkList': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['checkApp.CheckList']"}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'checkApp.template': {
            'Meta': {'object_name': 'Template'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pickledTasks': ('picklefield.fields.PickledObjectField', [], {'null': 'True'})
        }
    }

    complete_apps = ['checkApp']
