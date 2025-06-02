from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('conductor', 'Conductor'),
        ('admin', 'Administrador'),
        ('despachador','Despachador'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)

class Cliente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)

class Conductor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    licencia = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)

class Despachador(models.Model):
    user = models.OneToOneField(Usuario, on_delete = models.CASCADE)

class EstadoEntrega(models.Models):
    estado = models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)

class Sucursal(models.Models):
    comuna = models.CharField(max_length=50)
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)

class Viaje(models.Models):
    asignador = models.ForeignKey(Despachador,on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor,on_delete=models.CASCADE)
    origen = models.ForeignKey(Sucursal,on_delete=models.SET_NULL)

class Paquete(models.Models):
    fecha_registro = models.DateField(default=date.today)
    ancho = models.DecimalField(max_digits=7, decimal_places=3)
    alto = models.DecimalField(max_digits=7, decimal_places=3)
    largo = models.DecimalField(max_digits=7, decimal_places=3)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    estado_actual = models.ForeignKey(EstadoEntrega,on_delete=models.SET_NULL)
    viaje = models.ForeignKey(Viaje,on_delete=models.SET_NULL)
    destinatario = models.ForeignKey(Cliente,on_delete =models.PROTECT)
    destino = models.ForeignKey(Sucursal,on_delete=models.CASCADE)

class HistorialPaquete(models.Models):
    paquete = models.ForeignKey(Paquete,on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoEntrega,on_delete=models.SET_NULL)
    fecha = models.DateField(default=date.today())


