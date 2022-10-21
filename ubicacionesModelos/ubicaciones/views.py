from django.shortcuts import render
from multiprocessing import context
from tkinter.messagebox import RETRY
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from sklearn.datasets import make_blobs
from .models import franquicias as franquicias
from .models import poblaciones as poblacionesModelo
import pandas as pd
from sklearn.cluster import KMeans
import re
from django.views.decorators.csrf import csrf_exempt

def generateLocations(cantidad,inicio,final, centeros, dispersion):
    x, y = make_blobs(
                  n_samples = cantidad, 
                  n_features = 2, 
                  centers = centeros,
                  cluster_std=dispersion,
                  shuffle= True,  
                  center_box=(inicio,final),
                   random_state = 0)
    return x[:,0]


def generarKmeans(clusters, iteraciones, tolerancia, state):
    km = KMeans(
    n_clusters=clusters,
    init='random',
    max_iter=iteraciones,
    tol=tolerancia, 
    random_state=state
    )

    train_km = km.fit_predict(x)
    train_km
    return train_km


# Create your views here.
#
def index(request):
    return render(request, 'index.html')

def inicio(request):
    return render(request, 'inicio.html')

def ubicaciones(request):
    print("lo iniciamos")
    lista =  franquicias.objects.values()
    listo=list(lista)
    mydict= {
        'datos':listo
    }
    return render(request, 'ubicaciones.html', context = mydict)
@csrf_exempt
def agregarPoblaciones(request):
    lngInicio=int(request.GET["lngInicio"])
    lngFInal=int(request.GET["lngFinal"])
    latInicio=int(request.GET["latInicio"])
    latFInal=int(request.GET["latFinal"])
    cantidad=int(request.GET["cantidad"])
    centros=int(request.GET["centros"])
    dispersion=int(request.GET["centros"])
    longitudes=generateLocations(cantidad, lngInicio,lngFInal,centros,dispersion)
    latitudes=generateLocations(cantidad, latInicio,latFInal,centros,dispersion)
    strlong = ','.join(str(x) for x in longitudes)
    strlat = ','.join(str(x) for x in latitudes)
    poblacion= poblacionesModelo(
        longitudes=strlong,
        latitudes=strlat
    )
    poblacion.save()
    return render(request, 'poblaciones.html')

def crearKmeans(request):
    clusters=int(request.GET["clusters"])
    iteraciones=int(request.GET["iteraciones"])
    tolerancia=int(request.GET["tolerancia"])
    state=int(request.GET["state"])
    
    strlong = ','.join(str(x) for x in longitudes)
    strlat = ','.join(str(x) for x in latitudes)
    poblacion= poblacionesModelo(
        longitudes=strlong,
        latitudes=strlat
    )
    poblacion.save()
    return render(request, 'kmeans.html')

def poblaciones(request):

    return render(request, 'poblaciones.html')

def kmeans(request):
    longitudes=generateLocations(10,10,20,3,0.1)
    latitudes=generateLocations(10,10,20,3,0.1)
    return render(request, 'kmeans.html')

def metricas(request):
    PDB = pd.read_csv("apptest/database/pizzahut.csv")
    PDBTypes = PDB [['type','state']]
    PDBTypes1 =  PDBTypes[(PDBTypes['type'] == "Pizza Hut")]
    Conteo = PDBTypes1.value_counts(PDBTypes1["state"])
    ContDF = pd.DataFrame(Conteo)

    mydict2 ={
        'dfTypes': ContDF.to_html()
    }
    return render(request,"metricas.html", context=mydict2)
  
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
    
