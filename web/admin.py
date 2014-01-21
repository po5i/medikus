from django.contrib import admin
from web.models import *   
from django.contrib.gis import admin as gisadmin
from django.contrib.auth.admin import *


class LugarAdmin(gisadmin.OSMGeoAdmin):
  list_display = ('nombre','foursquare')

class SintomaAdmin(admin.ModelAdmin):
  filter_horizontal = ('sintomas',)
  list_display = ('nombre','sintomas_padres','especialidad')
  def sintomas_padres(self,obj):
    padres = []
    padres_str = ""
    for s in obj.sintomas.iterator():
      padres.append(s.nombre)
    if len(padres) > 0:
      padres_str = " - ".join(padres)
      padres_str = "["+padres_str+"]"
    return u'%s'%(padres_str)


admin.site.register(MaestroTipo)
admin.site.register(MaestroEspecialidad)
admin.site.register(MaestroSeguro)
admin.site.register(Lugar,LugarAdmin)
admin.site.register(Sintoma,SintomaAdmin)
