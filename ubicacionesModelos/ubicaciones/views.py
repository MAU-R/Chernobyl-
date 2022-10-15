from django.shortcuts import render
from multiprocessing import context
from tkinter.messagebox import RETRY
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from .models import *
import pandas as pd
import re
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
    
