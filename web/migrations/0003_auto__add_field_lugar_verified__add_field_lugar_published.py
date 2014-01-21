# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lugar.verified'
        db.add_column(u'web_lugar', 'verified',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lugar.published'
        db.add_column(u'web_lugar', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lugar.verified'
        db.delete_column(u'web_lugar', 'verified')

        # Deleting field 'Lugar.published'
        db.delete_column(u'web_lugar', 'published')


    models = {
        u'web.lugar': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Lugar'},
            'direccion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'emergencia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'especialidades': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.MaestroEspecialidad']", 'symmetrical': 'False'}),
            'farmacia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'foursquare': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagenologia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'laboratorio': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'seguros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.MaestroSeguro']", 'symmetrical': 'False'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.MaestroTipo']"}),
            'ubicacion': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'verified': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'web.maestroespecialidad': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'MaestroEspecialidad'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'web.maestroseguro': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'MaestroSeguro'},
            'direccion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'web.maestrotipo': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'MaestroTipo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'web.sintoma': {
            'Meta': {'object_name': 'Sintoma'},
            'especialidad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.MaestroEspecialidad']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'peso': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sintomas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['web.Sintoma']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['web']