from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView 

urlpatterns = [
    
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')), # <- JF
    path('paquetes-asignados/', views.pedidos_asignados_conductor, name='mis_pedidos'),
    path('asignar-paquetes/', views.asignar_paquetes, name='asignar_paquetes'),
    path('cambiar-estado/<int:paquete_id>/', views.cambiar_estado_paquete, name='cambiar_estado'),
    path('ver-viajes/', views.ver_viajes, name='ver_viajes'),
    path('estado-global/', views.ver_estado_global, name='estado_global'),
    path('registro/', views.registro_cliente, name='registro'),
    path('ver-paquetes/', views.pedidos_asignados_conductor, name='ver_paquetes'),
    path('', views.home, name='home'),
    path('crear-viaje/', views.crear_viaje, name = 'crear_viaje'),
    path('mis-viajes/', views.ver_viajes_conductor, name='mis_viajes'),
]

