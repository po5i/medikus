# coding=utf-8
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from web.models import *   
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.utils import simplejson
from django.core.mail import EmailMessage,EmailMultiAlternatives

def index(request):
    context = {'variable': "Hello"}
    return render(request, 'web/index.html', context)

@csrf_exempt
def atencion(request):
    #distance_from_point = {'km':'10'}
    latitud = request.GET.get('lat','-2.165731')    #default
    longitud = request.GET.get('lng','-79.892000')
    current_point = geos.fromstr("POINT(%s %s)" % (longitud, latitud))
    waypoints = Lugar.objects.all()                         #filter(ubicacion__distance_lte=(current_point, measure.D(**distance_from_point)))
    waypoints = waypoints.distance(current_point).order_by('distance')

    #maestros
    #especialidades = MaestroEspecialidad.objects.all()  #todos
    especialidades = MaestroEspecialidad.objects.filter(lugar__isnull=False).distinct()     #solo con datos
    tipos = MaestroTipo.objects.all()

    #pre-filters
    especialidad_id = request.GET.get('especialidad_id')
    tipo_id = request.GET.get('tipo_id')

    context = {
                'waypoints': waypoints,
                'latitud':latitud,
                'longitud':longitud,
                'especialidades':especialidades,
                'tipos':tipos,
                'prefilters': {
                                    'especialidad_id':especialidad_id,
                                    'tipo_id':tipo_id,
                }
    }
    return render(request, 'web/atencion.html',context)


def sintomas(request):
    return render(request, 'web/sintomas.html')

def especializacion(request):
    #especialidades = MaestroEspecialidad.objects.all()  #todos
    especialidades = MaestroEspecialidad.objects.filter(lugar__isnull=False).distinct()     #solo con datos
    context = {
                'especialidades':especialidades,
    }
    return render(request, 'web/especializacion.html',context)

def emergencia(request):
    return render(request, 'web/emergencia.html')

@csrf_exempt
def emergencia_mail(request):
    nombre = request.POST.get("nombre")
    telefono = request.POST.get("telefono")
    latitud = request.POST.get("latitud")
    longitud = request.POST.get("longitud")
    mapa = request.POST.get("mapa")
    gmap = "https://maps.google.com/maps?z=16&t=m&q="+latitud+","+longitud

    from_email = 'Medikus <medikus.ec@gmail.com>'
    subject = 'Alerta de emergencia enviada desde Medikus'
    tos = ["medikus.ec@gmail.com","gluzardo@cti.espol.edu.ec","saul.carpio@cti.espol.edu.ec"]
    message = ('<h2>Reporte de emergencia</h2>'
                    '<p>Nombre: '+nombre+'</p>'
                    '<p>Telefono: '+telefono+'</p>'
                    '<p>Latitud: '+latitud+'</p>'
                    '<p>Longitud: '+longitud+'</p>'
                    '<p>'+mapa+'</p>'
                    '<p>Google Maps: '+gmap+'</p>'
                    '<br/><p>Este mensaje ha sido generado autom&aacute;ticamente por Medikus</p>'
    )

    msg = EmailMultiAlternatives(subject, "", from_email,tos)
    msg.attach_alternative(message, "text/html")
    msg.send()
    return HttpResponse("OK", content_type="text/plain")

def filtro(request):
    #distance_from_point = {'km':'10'}
    especialidad_id = request.GET.get('especialidad_id')
    tipo_id = request.GET.get('tipo_id')
    latitud = request.GET.get('my_lat')
    longitud = request.GET.get('my_long')
    current_point = geos.fromstr("POINT(%s %s)" % (longitud, latitud))

    waypoints = Lugar.objects.all()

    if especialidad_id != "" and especialidad_id != None:
        especialidad_id = int(especialidad_id)
        waypoints = Lugar.objects.filter(especialidades__id__exact=especialidad_id)
    if tipo_id != "" and tipo_id != None:
        tipo_id = int(tipo_id)
        waypoints = Lugar.objects.filter(tipo__id__exact=tipo_id)

    waypoints = waypoints.distance(current_point).order_by('distance')

    return render(request, 'web/filtro.html',{'waypoints': waypoints})

def cargarSintomas(request):
    ubicacion = request.GET.get('ubic')
    mimetype = 'application/xml'
    cuerpo=Sintoma.objects.filter(pk=ubicacion)
    #cuerpo1=Sintoma.objects.filter(pk=12)	
    Sintomas=Sintoma.objects.filter(sintomas__in=cuerpo)
    #Sintomas=Sintoma.objects.filter(sintomas__in=cuerpo).filter(sintomas__in=cuerpo1)		
    data='<sintomas>'	
    if len(Sintomas)>0:
	for s in Sintomas:
            data+='<sintoma><nombre>'
            data+=s.nombre.encode('utf-8')+'</nombre><val>'
            data+=str(s.id)+'</val></sintoma>'
        data+='</sintomas>'
    else:
        for esp in cuerpo:
            data+='<sintoma><nombre>'
            data+=esp.especialidad.nombre.encode('utf-8')+'</nombre><val>'
            data+=str(esp.especialidad.id)+'</val></sintoma>'
	data+='<paso>3</paso>'
        data+='</sintomas>'        
    return HttpResponse(data,mimetype)

def generar_open_data(request):
    #data = {"hello":"world"}
    data = []
    lugares = Lugar.objects.all()
    for lugar in lugares:
        especialidades = []
        for esp in lugar.especialidades.iterator():
            especialidades.append({
                                    "nombre":str(esp)
                })
        seguros = []
        for seg in lugar.seguros.iterator():
            seguros.append({
                                    "nombre":str(seg)
                })
        data.append({
                        "nombre":lugar.nombre,
                        "direccion":lugar.direccion,
                        "latitud":lugar.ubicacion.y,
                        "longitud":lugar.ubicacion.x,
                        "telefono":lugar.telefono,
                        "emergencia":lugar.emergencia,
                        "farmacia":lugar.farmacia,
                        "laboratorio":lugar.laboratorio,
                        "imagenologia":lugar.imagenologia,
                        "tipo":str(lugar.tipo),
                        "especialidades":especialidades,
                        "seguros":seguros,
            })

    return HttpResponse(simplejson.dumps(data), mimetype='application/json;charset=UTF-8')
    	
def quienes(request):
    return render(request, 'web/quienes.html')

def ayuda(request):
    return render(request, 'web/ayuda.html')