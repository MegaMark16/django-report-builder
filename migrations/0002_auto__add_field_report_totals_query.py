# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Report.totals_query'
        db.add_column('report_builder_report', 'totals_query', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Report.totals_query'
        db.delete_column('report_builder_report', 'totals_query')


    models = {
        'report_builder.report': {
            'Meta': {'object_name': 'Report'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'totals_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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
