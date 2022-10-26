import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_longitude(x):
    plt.switch_backend('AGG')
    plt.figure(figsize=(6,5))
    plt.title('Longitudes')
    plt.hist(x, fc='k', ec='k', rwidth=0.85)
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_latitude(x):
    plt.switch_backend('AGG')
    plt.figure(figsize=(6,5))
    plt.title('Latitudes')
    plt.hist(x, fc='k', ec='k', rwidth=0.85)
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_codes(labels, sizes):
    plt.switch_backend('AGG')
    plt.figure(figsize=(6,5))
    plt.title('Identificador')
    plt.pie(sizes, labels=labels)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_transport(labels, sizes):
    plt.switch_backend('AGG')
    plt.figure(figsize=(11,7))
    plt.title('Transporte')
    plt.bar(labels, sizes)
    plt.xlabel('Tipo')
    plt.ylabel('En uso')
    plt.tight_layout()
    graph = get_graph()
    return graph