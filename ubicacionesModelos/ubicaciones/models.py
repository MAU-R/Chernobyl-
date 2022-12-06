from django.db import models
from django.shortcuts import redirect
import pandas as pd
import os
from django.conf import settings
from django.core.files import File

class franquicias(models.Model):
    Color=models.CharField(max_length=200)
    Nombre=models.CharField(max_length=200)
    Descripcion=models.CharField(max_length=100)
    latitud=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100   )    




class poblaciones(models.Model):
    longitudes=models.TextField()
    latitudes=models.TextField()

class kmeansOpciones(models.Model):
    clusters=models.IntegerField()
    tolerancia=models.FloatField()
    iteraciones=models.IntegerField()
    state=models.IntegerField()
    

class detalleKPoblaciones(models.Model):
    idPoblacion=models.IntegerField()
    idKmeans=models.IntegerField()

class KmeansEncuestaOpciones(models.Model):
    clusters=models.IntegerField()
    tolerancia=models.FloatField()
    iteraciones=models.IntegerField()
    state=models.IntegerField()

class svmoptions(models.Model):
    sueldo=models.BooleanField()
    stream=models.BooleanField()
    club=models.BooleanField()
    gasto=models.BooleanField()