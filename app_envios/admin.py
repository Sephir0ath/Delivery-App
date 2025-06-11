from django.contrib import admin
from .models import Usuario, Cliente, Conductor, Despachador, Paquete, Viaje, EstadoEntrega, HistorialPaquete, Sucursal

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Conductor)
admin.site.register(Despachador)
admin.site.register(Paquete)
admin.site.register(Viaje)
admin.site.register(EstadoEntrega)
admin.site.register(HistorialPaquete)
admin.site.register(Sucursal)
