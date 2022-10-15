from django.shortcuts import render
from multiprocessing import context
from tkinter.messagebox import RETRY
from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from .models import *
import pandas as pd
import re
# Create your views here.
def index(request):
    return render(request, 'index.html')

def inicio(request):
    return render(request, 'inicio.html')

def crear_ubicacion(request, color, nombre, descripcion,latitud, longitud):
    ubicacion = franquicias(
    Color=color,
    Nombre=nombre,
    Descripcion=descripcion,
    latitud=latitud,
    longitude=longitud
    )
    ubicacion.save()
    return HttpResponse("creado ubicacion creado")
def ubicaciones(request):
    print("lo iniciamos")
    lista =  franquicias.objects.values()
    listo=list(lista)
    print(listo)
    mydict= {
        'datos':listo
    }
    return render(request, 'ubicaciones.html', context = mydict)

def usuario(request,id):
    try:
        usuario = User.objects.get(pk=id)
        response = f"{usuario.name} - {usuario.lastn}"
    except:
        response = "El dato no se encuentra en la BD"
    return HttpResponse(response)

def editarUsuario(request,id):
    usuario = User.objects.get(pk=id)
    usuario.name = "Modificado"
    usuario.lastn =  "Modificado"

    usuario.save()

    return HttpResponse(f"Articulo editado con el id: {usuario.id}")

def usuarios(request):
    usuarios = User.objects.order_by("-name")
    return render(request
    ,'usuarios.html',{
        'usuarios':usuarios
    })


def eliminar(request,id):
    usuario = User.objects.get(pk=id)

    usuario.delete()

    return redirect('usuarios')
