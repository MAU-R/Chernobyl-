from django.db import models


class franquicias(models.Model):
    Color=models.CharField(max_length=200)
    Nombre=models.CharField(max_length=200)
    Descripcion=models.CharField(max_length=100)
    latitud=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)

class poblaciones(models.Model):
    longitudes=models.TextField()
    latitudes=models.TextField()

class kmeansOpciones(models.Model):
    longitudes=models.TextField()
    
class detalleKPoblaciones(models.Model):
    idPoblacion=models.IntegerField()
    idKmeans=models.IntegerField()