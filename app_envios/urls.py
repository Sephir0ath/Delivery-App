from django.urls import path
from . import views

urlpatterns = [
    path('mis-pedidos/', views.pedidos_asignados_conductor, name='mis_pedidos'),
    path('asignar-paquetes/', views.asignar_paquetes, name='asignar_paquetes'),
]