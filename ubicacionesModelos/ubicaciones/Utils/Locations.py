#imports 
import matplotlib.pyplot as plt 
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import pandas as pd
from ubicaciones.models import franquicias
import seaborn as sns
import base64
from io import BytesIO
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle

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
    random_state=45
    )
    wcss=generarElbow(x)
    train_km = km.fit_predict(x)
    return list(train_km), wcss

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
    
def datosEncuestas():
    datos = pd.read_excel("ubicaciones/database/datitos.xlsx");
    X=datos.iloc[:, [13,14]]
    return datos
def generarElbow(X):
    wcss = []
    for i in range(1, 15):
            kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 45)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
    return wcss

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def generarPlot(wcss):
    plt.figure(figsize=(10,5))
    sns.lineplot( wcss,marker='o',color='blue')
    plt.title('The Elbow Method')
    plt.xlabel('Clusters')
    plt.ylabel('WCSS')
    grap = get_graph()
    return grap

def trainEncuesta(datos, clusters,iteraciones,tolerancia,state):

    X=datos.iloc[:, [13,14]]
    import random
    for i in range(138):
        X['Latitud'][i]=(X['Latitud'][i]-random.uniform(0.01000, 0.00010))
        X['Longitud'][i]=(X['Longitud'][i]-random.uniform(0.01000, 0.00010))
    X=X.values
    train_km, wcss = generarKmeans(clusters, iteraciones, tolerancia,state, X)
    graph = generarPlot(wcss)
    return train_km , X ,graph

def generarSVM(sueldo,stream,club,gasto):
    datos = pd.read_excel("ubicaciones/database/datitos.xlsx");
    x=shuffle(datos)
    import random
    for i in range(138):
        x['Latitud'][i]=(x['Latitud'][i]-random.uniform(0.01000, 0.00010))
        x['Longitud'][i]=(x['Longitud'][i]-random.uniform(0.01000, 0.00010))
    X=x.iloc[0:97, [13,14]].values
    y= x['clase'].values
    datos= []
    for j in range((x.shape[0])):
        app=[]
        if(sueldo):
            app.append(x['Sueldo'][j])
        if(stream):
            app.append(x['membresiasStreaming'][j])
        if(club):
            app.append(x['plataforma'][j])
        if(gasto):
            app.append(x['gastos'][j])
        datos.append(app)
    print("Funcionan los datos???? -               -- ---")
    print(datos)
    x_train, x_test, y_train, y_test =train_test_split(datos, y, test_size=0.3, random_state=0,  shuffle=False)
    sc = StandardScaler()
    sc.fit(x_train)
    x_train_std = sc.transform(x_train)
    x_test_std = sc.transform(x_test)
    x_train_std
    svc = SVC(C=1.0, random_state=1, kernel='linear')
    # Entrenar modelo
    svc.fit(x_train_std, y_train)
    y_predict = svc.predict(x_train_std)
    return X, y_predict