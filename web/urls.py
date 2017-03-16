from django.conf.urls import  url

from web import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^atencion/$', views.atencion),
    url(r'^sintomas/$', views.sintomas),
    url(r'^especializacion/$', views.especializacion),
    url(r'^emergencia/$', views.emergencia),
    url(r'^filtro/$', views.filtro),
    url(r'^quienes/$', views.quienes),
    url(r'^ayuda/$', views.ayuda),
    url(r'^emergencia_mail/$', views.emergencia_mail),
    url(r'^generar_open_data/$', views.generar_open_data),
    url(r'^cargarSintomas/$', views.cargarSintomas),
    url(r'^store/$', views.store),
]
