# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MaestroTipo'
        db.create_table(u'web_maestrotipo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'web', ['MaestroTipo'])

        # Adding model 'MaestroEspecialidad'
        db.create_table(u'web_maestroespecialidad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'web', ['MaestroEspecialidad'])

        # Adding model 'MaestroSeguro'
        db.create_table(u'web_maestroseguro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['MaestroSeguro'])

        # Adding model 'Lugar'
        db.create_table(u'web_lugar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('direccion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ubicacion', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('emergencia', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.MaestroTipo'])),
            ('farmacia', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('laboratorio', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('imagenologia', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Lugar'])

        # Adding M2M table for field especialidades on 'Lugar'
        m2m_table_name = db.shorten_name(u'web_lugar_especialidades')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lugar', models.ForeignKey(orm[u'web.lugar'], null=False)),
            ('maestroespecialidad', models.ForeignKey(orm[u'web.maestroespecialidad'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lugar_id', 'maestroespecialidad_id'])

        # Adding M2M table for field seguros on 'Lugar'
        m2m_table_name = db.shorten_name(u'web_lugar_seguros')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lugar', models.ForeignKey(orm[u'web.lugar'], null=False)),
            ('maestroseguro', models.ForeignKey(orm[u'web.maestroseguro'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lugar_id', 'maestroseguro_id'])

        # Adding model 'Sintoma'
        db.create_table(u'web_sintoma', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('peso', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('especialidad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.MaestroEspecialidad'], null=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Sintoma'])

        # Adding M2M table for field sintomas on 'Sintoma'
        m2m_table_name = db.shorten_name(u'web_sintoma_sintomas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_sintoma', models.ForeignKey(orm[u'web.sintoma'], null=False)),
            ('to_sintoma', models.ForeignKey(orm[u'web.sintoma'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_sintoma_id', 'to_sintoma_id'])


    def backwards(self, orm):
        # Deleting model 'MaestroTipo'
        db.delete_table(u'web_maestrotipo')

        # Deleting model 'MaestroEspecialidad'
        db.delete_table(u'web_maestroespecialidad')

        # Deleting model 'MaestroSeguro'
        db.delete_table(u'web_maestroseguro')

        # Deleting model 'Lugar'
        db.delete_table(u'web_lugar')

        # Removing M2M table for field especialidades on 'Lugar'
        db.delete_table(db.shorten_name(u'web_lugar_especialidades'))

        # Removing M2M table for field seguros on 'Lugar'
        db.delete_table(db.shorten_name(u'web_lugar_seguros'))

        # Deleting model 'Sintoma'
        db.delete_table(u'web_sintoma')

        # Removing M2M table for field sintomas on 'Sintoma'
        db.delete_table(db.shorten_name(u'web_sintoma_sintomas'))


    models = {
        u'web.lugar': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Lugar'},
            'direccion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'emergencia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'especialidades': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.MaestroEspecialidad']", 'symmetrical': 'False'}),
            'farmacia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagenologia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'laboratorio': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'seguros': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.MaestroSeguro']", 'symmetrical': 'False'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.MaestroTipo']"}),
            'ubicacion': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'})
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