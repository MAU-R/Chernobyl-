from django.shortcuts import render
from multiprocessing import context
from tkinter.messagebox import RETRY
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from sklearn.datasets import make_blobs
from .models import franquicias as franquicias, kmeansOpciones
from .models import poblaciones as poblacionesModelo
import pandas as pd
import numpy 
from sklearn.cluster import KMeans
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


def generateLocations2(cantidad,inicio,final,inicioln,finallng, centeros, dispersion):
    x, y = make_blobs(
                  n_samples = cantidad, 
                  n_features = 2, 
                  centers = centeros,
                  cluster_std=dispersion,
                  shuffle= True,  
                  center_box=([inicio,inicioln],[final,finallng]),
                   random_state = 0)
    return x

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
    lngInicio=float(request.GET["lngInicio"])
    lngFInal=float(request.GET["lngFinal"])
    latInicio=float(request.GET["latInicio"])
    latFInal=float(request.GET["latFinal"])
    cantidad=int(request.GET["cantidad"])
    centros=int(request.GET["centros"])
    dispersion=float(request.GET["centros"])
    cordenadas=generateLocations2(cantidad, latInicio,latFInal,lngInicio,lngFInal,centros,dispersion)
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


def poblaciones(request):
    locaciones=poblacionesModelo.objects.all()
    return render(request, 'poblaciones.html' ,{"locaciones": locaciones})


def kmeans(request):
    if(kmeansOpciones.objects.last()):
        kmeans= kmeansOpciones.objects.last()
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


def eliminadoDefinitivo(request):
   pobs=poblacionesModelo.objects.all().delete()
   k=kmeansOpciones.objects.all().delete()

   return redirect(inicio)
