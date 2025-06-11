# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('viaje/<int:viaje_id>/ruta/', views.optimizar_ruta, name='optimizar_ruta'),
]
