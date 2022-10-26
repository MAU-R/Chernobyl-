"""ubicacionesModelos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from operator import index
from django.contrib import admin
from django.urls import path
from ubicaciones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.inicio, name = "index"),
    path("inicio/", views.inicio, name="inicio"),
    path("ubicaciones/", views.ubicaciones, name="ubicaciones"),
    path("poblaciones/", views.poblaciones, name="poblacion"),
    path("customMap/", views.kmeans, name="kmeans"),
    path("graficas/", views.graficas, name="graficas"),
    path("crearPoblaciones/", views.agregarPoblaciones, name="crearPoblacion"),
    path("crearKmeans/", views.crearKmeans, name="crearKmeans"),
    path("eliminadoDefinitivo/", views.eliminadoDefinitivo, name="borrador"),
    path("crearUbicacion/<str:color>/<str:nombre>/<str:descripcion>/<str:longitud>/<str:latitud>", views.crear_ubicacion, name="crear-ubicacion"),
    path("actualizar/<int:id>/<str:color>/<str:nombre>/<str:descripcion>/<str:longitud>/<str:latitud>", views.actualizar_ubicacion, name="crear-ubicacion"),
    path("eliminar/<int:id>",views.eliminar,name="eliminar")

]
