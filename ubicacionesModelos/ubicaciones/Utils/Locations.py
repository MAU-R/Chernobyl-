#imports 
import matplotlib.pyplot as plt 
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def generateLocations(cantidad,lngInicio, lngFinal, latInicio, latFinal, centers, dispersion):
    x, y = make_blobs(n_samples = cantidad, 
                  n_features = 2, 
                  centers = centers,
                  cluster_std=dispersion,
                  shuffle= True,  
                  center_box=([lngInicio,lngFinal], [latInicio,latFinal]), 
                   random_state = 0)
    print(x);

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

def generarKmeans(clusters, iteraciones, tolerancia, state, x):
    km = KMeans(
    n_clusters=clusters,
    init='random',
    max_iter=iteraciones,
    tol=tolerancia, 
    random_state=0
    )
    train_km = km.fit_predict(x)
    return list(train_km)

def conseguirFranquiciasDeExcel():
    dt = pd.read_csv("ubicaciones/database/pizzahut.csv")
    nombres=dt["type"]
    latitudes=dt["latitude"]
    longitudes=dt["longitude"]
    descripciones=dt["address_1"]
    for x in range(0, 6000, 15):
        ubicacion=franquicias(
          Color="#FFFFF",
          Nombre=nombres[x],
          Descripcion=descripciones[x],
          latitud=latitudes[x],
          longitude=longitudes[x]  
          )
        ubicacion.save()
    