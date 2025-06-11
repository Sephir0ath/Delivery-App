from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('conductor', 'Conductor'),
        ('admin', 'Administrador'),
        ('despachador','Despachador'),
    )
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Cambia esto para evitar colisiones
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',  # Cambia esto también
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Cliente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)

class Conductor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    licencia = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)

class Despachador(models.Model):
    user = models.OneToOneField(Usuario, on_delete = models.CASCADE)