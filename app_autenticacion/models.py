from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class Sucursal(models.Model):
    comuna = models.CharField(max_length=50)
    latitud = models.FloatField()
    longitud = models.FloatField()
    def __str__(self):
        return self.comuna

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('conductor', 'Conductor'),
        ('admin', 'Administrador'),
        ('despachador','Despachador'),
    )
    #email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    def __str__(self):
        return self.username
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

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
    def __str__(self):
        return self.user.username

class Conductor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    licencia = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    sucursal =  models.ForeignKey(Sucursal,on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

class Despachador(models.Model):
    user = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    def __str__(self):
        return self.user.username