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

    