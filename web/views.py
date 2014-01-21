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

def browse_foursquare(latitud,longitud):
    #waypoints = Lugar.objects.all()
    waypoints = []
    dummy_id = 0

    import urllib2
    import json

    url = "https://api.foursquare.com/v2/venues/search?ll="+latitud+","+longitud+"&client_id=CE4CTYXWWAXMD2GIHVTEF21CPIWRRDBEV5SHHP5ZHQVQWXS0&client_secret=JSSJUHGBJCTTYJMJKXUOFZQNZFKC31VN2DZUQEATMTISZNCI&v=20140113&intent=browse&radius=10000&categoryId=4bf58dd8d48988d104941735"
    f = urllib2.urlopen(url)
    response = f.read()
    response_json = json.loads(response)

    for res in response_json["response"]["venues"]:
        dummy_id = dummy_id + 1

        #check in the database for more metadata
        lugar = Lugar.objects.filter(foursquare=res["id"])[:1]       

        if "crossStreet" in res["location"]:
            direccion = res["location"]["address"]+" & "+res["location"]["crossStreet"]
        elif "address" in res["location"]:
            direccion = res["location"]["address"]
        else:
            direccion = lugar[0].direccion if lugar else ""

        way = {                
                'id':dummy_id,
                'foursquare':res["id"],
                'nombre':res["name"],
                'latitud':res["location"]["lat"],
                'longitud':res["location"]["lng"],
                'distance':res["location"]["distance"],
                'direccion':direccion,
                #'direccion':lugar[0].direccion if lugar else "",
                'telefono':lugar[0].telefono if lugar else "",
                'emergencia':lugar[0].emergencia if lugar else "",
                'tipo':lugar[0].tipo if lugar else "",
                'imagenologia':lugar[0].imagenologia if lugar else "",
                'laboratorio':lugar[0].laboratorio if lugar else "",
                'farmacia':lugar[0].farmacia if lugar else "",
                'seguros':lugar[0].seguros_csv if lugar else "",
                'source': 'local' if lugar else '4sq',
        }
        waypoints.append(way)

    return waypoints


def normalize_waypoins(waypoints):
    out = []
    for wp in waypoints:
        way = {                
                'id':wp.id,
                'foursquare':wp.foursquare,
                'nombre':wp.nombre,
                'latitud':wp.ubicacion.y,
                'longitud':wp.ubicacion.x,
                'distance':wp.distance if wp.distance else 0,
                'direccion':wp.direccion,
                'telefono':wp.telefono,
                'emergencia':wp.emergencia,
                'tipo':wp.tipo,
                'imagenologia':wp.imagenologia ,
                'laboratorio':wp.laboratorio,
                'farmacia':wp.farmacia,
                'seguros':wp.seguros_csv,
                'source': 'local',
        }
        out.append(way)

    return out



@csrf_exempt
def atencion(request):
    #distance_from_point = {'km':'10'}
    latitud = request.GET.get('lat','-2.165731')    #default
    longitud = request.GET.get('lng','-79.892000')
    current_point = geos.fromstr("POINT(%s %s)" % (longitud, latitud))
    #waypoints = Lugar.objects.all()                         #filter(ubicacion__distance_lte=(current_point, measure.D(**distance_from_point)))
    #waypoints = waypoints.distance(current_point).order_by('distance')

    waypoints = browse_foursquare(latitud,longitud)

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

    #waypoints = Lugar.objects.all()
    waypoints = browse_foursquare(latitud,longitud)
    
    #Si el usuario quiere datos filtrados, no se usaría 4sq
    if especialidad_id != "" and especialidad_id != None:
        especialidad_id = int(especialidad_id)
        waypoints = Lugar.objects.filter(especialidades__id__exact=especialidad_id)
        waypoints = waypoints.distance(current_point).order_by('distance')
        waypoints = normalize_waypoins(waypoints)
    if tipo_id != "" and tipo_id != None:
        tipo_id = int(tipo_id)
        waypoints = Lugar.objects.filter(tipo__id__exact=tipo_id)
        waypoints = waypoints.distance(current_point).order_by('distance')    
        waypoints = normalize_waypoins(waypoints)
    
    return render(request, 'web/filtro.html',{'waypoints': waypoints})  #,content_type='application/json'

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
                        "foursquare_id":lugar.foursquare,
            })

    return HttpResponse(simplejson.dumps(data), mimetype='application/json;charset=UTF-8')
    	
def quienes(request):
    return render(request, 'web/quienes.html')

def ayuda(request):
    return render(request, 'web/ayuda.html')

@csrf_exempt
def store(request):
    nombre = request.POST.get("nombre")
    direccion = request.POST.get("direccion")
    lat = request.POST.get("lat")
    lng = request.POST.get("lng")
    telefono = request.POST.get("telefono")
    emergencia = int(request.POST.get("emergencia"))
    imagenologia = int(request.POST.get("imagenologia"))
    laboratorio = int(request.POST.get("laboratorio"))
    farmacia = int(request.POST.get("farmacia"))
    tipo = request.POST.get("tipo")
    foursquare_id = request.POST.get("foursquare_id")

    try:
        lugar = Lugar.objects.get(foursquare=foursquare_id)
        lugar.nombre = nombre
        lugar.telefono = telefono
        lugar.emergencia = emergencia
        lugar.imagenologia = imagenologia
        lugar.laboratorio = laboratorio
        lugar.tipo_id = tipo_id
        lugar.save()
    except Lugar.DoesNotExist:
        lugar = Lugar(
                        nombre=nombre,
                        direccion=direccion,
                        ubicacion="POINT ("+lng+" "+lat+")",
                        telefono=telefono,
                        emergencia=emergencia,
                        imagenologia=imagenologia,
                        laboratorio=laboratorio,
                        farmacia=farmacia,
                        tipo_id=tipo,
                        foursquare=foursquare_id,
        )
        lugar.save()
    
    """
    from_email = 'Medikus <medikus.ec@gmail.com>'
    subject = 'Notificación de nueva metadata'
    tos = ["medikus.ec@gmail.com"]
    message = ('<h2>Nueva metadata ingresada</h2>'
                    '<p>Nombre: '+nombre+'</p>'
                    '<p>Telefono: '+telefono+'</p>'
                    '<p>Foursquare_id: '+foursquare_id+'</p>'
                    '<br/><p>Este mensaje ha sido generado autom&aacute;ticamente por Medikus</p>'
    )

    msg = EmailMultiAlternatives(subject, "", from_email,tos)
    msg.attach_alternative(message, "text/html")
    msg.send()
    """
    return HttpResponse("OK", content_type="text/plain")