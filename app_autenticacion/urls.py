
from django.urls import path
from .views import register_cliente, register_conductor, login_view

urlpatterns = [
    path('registro/cliente/', register_cliente, name='register_cliente'),
    path('registro/conductor/', register_conductor, name='register_conductor'),
    path('login/', login_view, name='login'),
]
