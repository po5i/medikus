from django.db import models
#from django.contrib.auth.models import  User
from django.contrib.gis.db import models


# Create your models here.

class MaestroTipo(models.Model):
  nombre = models.CharField(max_length=50)
  def __unicode__(self):
    return u'%s'%(self.nombre) 
  class Meta:
    ordering = ['nombre']
    verbose_name_plural = "Maestro tipos"

class MaestroEspecialidad(models.Model):
  nombre = models.CharField(max_length=50)
  def __unicode__(self):
    return u'%s'%(self.nombre)
  def badge(self):
    count = Lugar.objects.filter(especialidades__id__exact=self.id).count()
    return count
  class Meta: 
    ordering = ['nombre']
    verbose_name_plural = "Maestro especialidades"

class MaestroSeguro(models.Model):
  nombre = models.CharField(max_length=50)
  direccion = models.TextField(null=True, blank=True)
  telefono = models.CharField(max_length=128,null=True,blank=True)
  def __unicode__(self):
    return u'%s'%(self.nombre)
  class Meta: 
    ordering = ['nombre']
    verbose_name_plural = "Maestro seguros"



class Lugar(models.Model):
  nombre = models.CharField(max_length=256)
  direccion = models.TextField(null=True, blank=True)
  ubicacion = models.PointField(null=True,blank=True)
  objects = models.GeoManager()
  telefono = models.CharField(max_length=128,null=True,blank=True)
  emergencia = models.NullBooleanField(null=True,blank=True)
  tipo = models.ForeignKey(MaestroTipo)
  farmacia = models.NullBooleanField(null=True,blank=True)
  laboratorio = models.NullBooleanField(null=True,blank=True)
  imagenologia = models.NullBooleanField(null=True,blank=True)
  especialidades = models.ManyToManyField(MaestroEspecialidad)
  seguros = models.ManyToManyField(MaestroSeguro)
  foursquare = models.CharField(max_length=256,default="",null=True,blank=True)
  verified = models.BooleanField(default=False)
  published = models.BooleanField(default=True)

  def __unicode__(self):
    return u'%s'%(self.nombre)
  def latitud(self):
    return str(self.ubicacion.y).replace(",",".")
  def longitud(self):
    return str(self.ubicacion.x).replace(",",".")
  def seguros_csv(self):
    val = []
    for s in self.seguros.iterator():
      val.append(s.nombre)
    val_csv = ", ".join(val)
    return val_csv
  class Meta: 
    ordering = ['nombre']
    verbose_name_plural = "Lugares"


class Sintoma(models.Model):
  sintomas = models.ManyToManyField("self", symmetrical=False,null=True,blank=True)
  nombre = models.CharField(max_length=256)
  peso = models.FloatField(null=True,blank=True)
  especialidad = models.ForeignKey(MaestroEspecialidad,null=True,blank=True)
  def __unicode__(self):
    #padres = []
    #padres_str = ""
    #for s in self.sintomas.iterator():
    #  padres.append(s.nombre)
    #if len(padres) > 0:
    #  padres_str = " - ".join(padres)
    #  padres_str = "["+padres_str+"]"
    #return u'%s %s'%(self.nombre,padres_str)
    return u'%s'%(self.nombre)
