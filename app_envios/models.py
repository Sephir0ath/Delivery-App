from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

from app_autenticacion.models import *


# Create your models here.

class EstadoEntrega(models.Model):
    estado = models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)

    def __str__(self):
        return self.estado

class Viaje(models.Model):
    asignador = models.ForeignKey(Despachador,on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor,on_delete=models.CASCADE)
    origen = models.ForeignKey(Sucursal,on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str(self.id)

class Paquete(models.Model):
    fecha_registro = models.DateField(default=date.today)
    ancho = models.DecimalField(max_digits=7, decimal_places=3)
    alto = models.DecimalField(max_digits=7, decimal_places=3)
    largo = models.DecimalField(max_digits=7, decimal_places=3)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    estado_actual = models.ForeignKey(EstadoEntrega,on_delete=models.SET_NULL, null=True, blank=True)
    viaje = models.ForeignKey(Viaje,on_delete=models.SET_NULL, null=True, blank=True)
    destinatario = models.ForeignKey(Cliente,on_delete =models.PROTECT)
    destino = models.ForeignKey(Sucursal,on_delete=models.SET_NULL, null=True, related_name='paquete')
    origen = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True,related_name='paquetes_origen')
    def __str__(self):
        return str(self.id)


class HistorialPaquete(models.Model):
    paquete = models.ForeignKey(Paquete,on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoEntrega,on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(default=timezone.now)
    def __str__(self):
        return self.paquete + self.estado


