# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-16 16:55
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('ubicacion', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('telefono', models.CharField(blank=True, max_length=128, null=True)),
                ('emergencia', models.NullBooleanField()),
                ('farmacia', models.NullBooleanField()),
                ('laboratorio', models.NullBooleanField()),
                ('imagenologia', models.NullBooleanField()),
                ('foursquare', models.CharField(blank=True, default=b'', max_length=256, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Lugares',
            },
        ),
        migrations.CreateModel(
            name='MaestroEspecialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Maestro especialidades',
            },
        ),
        migrations.CreateModel(
            name='MaestroSeguro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('telefono', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Maestro seguros',
            },
        ),
        migrations.CreateModel(
            name='MaestroTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Maestro tipos',
            },
        ),
        migrations.CreateModel(
            name='Sintoma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('peso', models.FloatField(blank=True, null=True)),
                ('especialidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.MaestroEspecialidad')),
                ('sintomas', models.ManyToManyField(blank=True, null=True, to='web.Sintoma')),
            ],
        ),
        migrations.AddField(
            model_name='lugar',
            name='especialidades',
            field=models.ManyToManyField(to='web.MaestroEspecialidad'),
        ),
        migrations.AddField(
            model_name='lugar',
            name='seguros',
            field=models.ManyToManyField(to='web.MaestroSeguro'),
        ),
        migrations.AddField(
            model_name='lugar',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.MaestroTipo'),
        ),
    ]
