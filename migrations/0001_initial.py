# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Report'
        db.create_table('report_builder_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('query', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('report_builder', ['Report'])

        # Adding model 'ReportParameter'
        db.create_table('report_builder_reportparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['report_builder.Report'])),
            ('parameter_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('list_items', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('default_value', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('report_builder', ['ReportParameter'])


    def backwards(self, orm):
        
        # Deleting model 'Report'
        db.delete_table('report_builder_report')

        # Deleting model 'ReportParameter'
        db.delete_table('report_builder_reportparameter')


    models = {
        'report_builder.report': {
            'Meta': {'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'query': ('django.db.models.fields.TextField', [], {})
        },
        'report_builder.reportparameter': {
            'Meta': {'object_name': 'ReportParameter'},
            'default_value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'list_items': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'parameter_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['report_builder.Report']"})
        }
    }

    complete_apps = ['report_builder']
