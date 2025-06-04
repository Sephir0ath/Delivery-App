from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Usuario, Cliente, Conductor, Despachador, EstadoEntrega,
    Sucursal, Viaje, Paquete, HistorialPaquete
)
from django.contrib.auth.admin import UserAdmin


@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('tipo',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('tipo',)}),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion')
    search_fields = ('user__username', 'direccion')


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('user', 'licencia', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('user__username', 'licencia')


@admin.register(Despachador)
class DespachadorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(EstadoEntrega)
class EstadoEntregaAdmin(admin.ModelAdmin):
    list_display = ('estado', 'descripcion')
    search_fields = ('estado',)


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('comuna', 'latitud', 'longitud')
    search_fields = ('comuna',)


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('asignador', 'conductor', 'origen')
    search_fields = ('asignador__user__username', 'conductor__user__username')


@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('fecha_registro', 'peso', 'destinatario', 'destino', 'estado_actual', 'viaje')
    list_filter = ('estado_actual', 'fecha_registro')
    search_fields = ('destinatario__user__username',)


@admin.register(HistorialPaquete)
class HistorialPaqueteAdmin(admin.ModelAdmin):
    list_display = ('paquete', 'estado', 'fecha')
    list_filter = ('estado', 'fecha')
