from concurrent.futures import process
from django.shortcuts import render
from multiprocessing import context
from tkinter.messagebox import RETRY
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from matplotlib.pyplot import axis
from sklearn import cluster
from sklearn.datasets import make_blobs
from .models import franquicias as franquicias, kmeansOpciones, KmeansEncuestaOpciones
from .models import poblaciones as poblacionesModelo
import pandas as pd
import numpy 
from sklearn.cluster import KMeans, cluster_optics_dbscan
from django.views.decorators.csrf import csrf_exempt
from .Utils import Locations as loc

from .Utils.plots import *
from more_itertools import split_before
# Create your views here.
#
def index(request):
    return render(request, 'index.html')

def inicio(request):
    return render(request, 'inicio.html')

def ubicaciones(request):
    x=franquicias.objects.all()
    print("Valores")
    print(x.values())
    if not x:
        print("amonos")
        loc.conseguirFranquiciasDeExcel()
    lista =  franquicias.objects.values()
    listo=list(lista)
    mydict= {
        'datos':listo
    }
    return render(request, 'ubicaciones.html', context = mydict)

@csrf_exempt
def agregarPoblaciones(request):
    lngInicio=float(request.GET["lngInicio"])
    lngFInal=float(request.GET["lngFinal"])
    latInicio=float(request.GET["latInicio"])
    latFInal=float(request.GET["latFinal"])
    cantidad=int(request.GET["cantidad"])
    centros=int(request.GET["centros"])
    dispersion=float(request.GET["centros"])
    cordenadas=loc.generateLocations2(cantidad, latInicio,latFInal,lngInicio,lngFInal,centros,dispersion)
    longitudes=cordenadas[:,1]
    latitudes=cordenadas[:,0]
    strlong = ','.join(str(x) for x in longitudes)
    strlat = ','.join(str(x) for x in latitudes)
    poblacion= poblacionesModelo(
        longitudes=strlong,
        latitudes=strlat
    )
    poblacion.save()
    return redirect(poblaciones)


@csrf_exempt
def crearKmeans(request):
    clusters=int(request.POST["numero"])
    iteraciones=int(request.POST["iteraciones"])
    tolerancia=float(request.POST["tolerancia"])
    state=int(request.POST["state"])

    kmeansModelo=kmeansOpciones(
    clusters=clusters,
    tolerancia=tolerancia,
    iteraciones=iteraciones,
    state=state
    )
    kmeansModelo.save()
    return redirect(kmeans)

@csrf_exempt
def crearKmeansenc(request):
    print("creamos kmeans encuesta")
    clusters=int(request.POST["numero"])
    iteraciones=int(request.POST["iteraciones"])
    tolerancia=float(request.POST["tolerancia"])
    state=int(request.POST["state"])

    kmeansModelo=KmeansEncuestaOpciones(
    clusters=clusters,
    tolerancia=tolerancia,
    iteraciones=iteraciones,
    state=state
    )
    kmeansModelo.save()
    return redirect(kmeansenc)

def poblaciones(request):
    locaciones=poblacionesModelo.objects.all()
    return render(request, 'poblaciones.html' ,{"locaciones": locaciones})


def kmeans(request):
    locaciones=poblacionesModelo.objects.all()
    kmeans= kmeansOpciones.objects.all()
    listaKmeans=kmeans.values()
    #print(locaciones.values()[1]["longitudes"])
    clusters=[]
    processed=[]
    for kmop in listaKmeans:
        clu=[]
        arreglox = []
        for ubicacion in locaciones:
            latitudes = ubicacion.latitudes.split(",")
            longitudes = ubicacion.longitudes.split(",")
            for x in range(len(longitudes)):
                arreglox.append([float(latitudes[x]), float(longitudes[x])])
        clu=loc.generarKmeans(int(kmop["clusters"]), int(kmop["iteraciones"]), float(kmop["tolerancia"]), float(kmop["state"]),arreglox)
        for valor in clu:
            clusters.append(valor)    
        clusters.append("/")
        #print("---------NUEVO----------")
        processed = [sublist for sublist in split_before(clusters, lambda i: i == '/')]
        for x in range(len(processed)):
            if '/' in processed[x]:
                processed[x].remove('/')
        print("---------COMO----------")
        print(processed)
    #clusters= loc.generarKmeans(clusters, iteraciones, tolerancia, state, x)
    return render(request, 'kmeans.html',{"locaciones": locaciones,"kmeans":kmeans, "centros":list(processed)})


def graficas(request):
    df = franquicias.objects.all()
    x1 = [x.longitude for x in df]
    x2 = [x.latitud for x in df]
    labels1 = []
    sizes1 = []
    labels2 = []
    sizes2 = []
    longitude = get_longitude(x1)
    latitude = get_latitude(x2)
    code = get_codes(labels1, sizes1)
    transport = get_transport(labels2, sizes2)
    
    mydict = {
        'longitude': longitude, 
        'latitude': latitude,
        'code': code,
        'transport': transport
    }
    return render (request, 'graficas.html', context=mydict)
  

#http://127.0.0.1:8000/crearUbicacion/color/mau/aqui/10/10
def crear_ubicacion(request, color, nombre, descripcion,latitud, longitud):
    gato="#"
    gato+=color
    print(gato)
    ubicacion = franquicias(
    Color=gato,
    Nombre=nombre,
    Descripcion=descripcion,
    latitud=latitud,
    longitude=longitud  
    )
    ubicacion.save()
    return HttpResponse("creado ubicacion creado")


def actualizar_ubicacion(request,id, color, nombre, descripcion,latitud, longitud):
    ubicacion= franquicias.objects.get(pk=id)
    print(descripcion)
    ubicacion.Color=color,
    ubicacion.Nombre=nombre,
    ubicacion.Descripcion=descripcion,
    ubicacion.latitud=latitud,
    ubicacion.longitude=longitud
    ubicacion.save()
    return HttpResponse("actualizado ubicacion actualizado")


def eliminar(request,id):
    ubicacion= franquicias.objects.get(pk=id)

    ubicacion.delete()
    return HttpResponse("borrado ubicacion borrado")


def eliminadoDefinitivo(request):
   poblacionesModelo.objects.all().delete()
   kmeansOpciones.objects.all().delete()
   franquicias.objects.all().delete()

   return redirect(inicio)


def kmeansenc(request):

    datos= loc.datosEncuestas()
    kmeans=KmeansEncuestaOpciones.objects.all().order_by('-id')[0]
    
    trained, ubicaciones, graph=loc.trainEncuesta(datos, kmeans.clusters, kmeans.iteraciones, kmeans.tolerancia,kmeans.state)
    Longitudes=[]
    Latitudes=[]
    for i in range(ubicaciones.shape[0]):
        Longitudes.append(ubicaciones[i][0])
        Latitudes.append(ubicaciones[i][1])
    print(Latitudes)
    #clusters= loc.generarKmeans(clusters, iteraciones, tolerancia, state, x)
    return render(request, 'kmeansenc.html', {"latitudes": Latitudes,"longitudes":Longitudes, "kmeans":trained, "elbow": graph})

def svm(request):

    ubicaciones, svm= loc.generarSVM()
    Longitudes=[]
    Latitudes=[]
    clasificacion=[]
    for i in range(ubicaciones.shape[0]):
        Longitudes.append(ubicaciones[i][0])
        Latitudes.append(ubicaciones[i][1])
        clasificacion.append(svm[i])
    print("Latitudes aquisssssssssssssssssssssssssssssssssssssss")
    print(clasificacion)
    return render(request, 'svm.html',{"latitudes": Latitudes,"longitudes":Longitudes,"svm":clasificacion})