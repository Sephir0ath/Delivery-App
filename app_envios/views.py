from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import (
    Conductor, Paquete, Sucursal, Despachador, Viaje, EstadoEntrega,
    HistorialPaquete, Cliente
)
from .forms import RegistroClienteForm

# Vista conductor: ver pedidos
@login_required
def pedidos_asignados_conductor(request):
    try:
        conductor = Conductor.objects.get(user=request.user)
    except Conductor.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No eres un conductor registrado."})

    paquetes = Paquete.objects.select_related('viaje', 'destino', 'destinatario').filter(viaje__conductor=conductor)
    return render(request, "conductor/paquetes_asignados.html", {"paquetes": paquetes})

# Vista despachador: asignar paquetes
@login_required
def asignar_paquetes(request):
    try:
        despachador = Despachador.objects.get(user=request.user)
    except Despachador.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No tienes permisos de despachador."})

    if request.method == 'POST':
        conductor_id = request.POST.get('conductor')
        sucursal_id = request.POST.get('sucursal')
        paquetes_ids = request.POST.getlist('paquetes')

        if not conductor_id or not sucursal_id or not paquetes_ids:
            return render(request, "error.html", {"mensaje": "Faltan datos para asignar."})

        try:
            conductor = Conductor.objects.get(id=conductor_id, disponible=True)
            sucursal = Sucursal.objects.get(id=sucursal_id)
            paquetes = Paquete.objects.filter(id__in=paquetes_ids, viaje__isnull=True)

            if not paquetes.exists():
                return render(request, "error.html", {"mensaje": "Los paquetes ya están asignados o no existen."})

            with transaction.atomic():
                viaje = Viaje.objects.create(asignador=despachador, conductor=conductor, origen=sucursal)
                paquetes.update(viaje=viaje)

            return redirect('despachador/asignar_paquetes')

        except (Conductor.DoesNotExist, Sucursal.DoesNotExist):
            return render(request, "error.html", {"mensaje": "Selección inválida."})

    paquetes_sin_asignar = Paquete.objects.filter(viaje__isnull=True).select_related('destinatario', 'destino')
    conductores_disponibles = Conductor.objects.filter(disponible=True).select_related('user')
    sucursales = Sucursal.objects.all()

    return render(request, "despachador/asignar_paquetes.html", {
        'paquetes': paquetes_sin_asignar,
        'conductores': conductores_disponibles,
        'sucursales': sucursales
    })

# Vista conductor: cambiar estado del paquete
@login_required
def cambiar_estado_paquete(request, paquete_id):
    try:
        conductor = Conductor.objects.get(user=request.user)
    except Conductor.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No eres un conductor autorizado."})

    paquete = get_object_or_404(Paquete, id=paquete_id, viaje__conductor=conductor)

    if request.method == 'POST':
        estado_id = request.POST.get('estado')
        nuevo_estado = get_object_or_404(EstadoEntrega, id=estado_id)
        paquete.estado_actual = nuevo_estado
        paquete.save()
        HistorialPaquete.objects.create(paquete=paquete, estado=nuevo_estado)
        return redirect('mis_pedidos')

    estados = EstadoEntrega.objects.all()
    return render(request, "conductor/cambiar_estado.html", {
        "paquete": paquete,
        "estados": estados
    })

# Vista despachador: ver viajes asignados
@login_required
def ver_viajes(request):
    try:
        despachador = Despachador.objects.get(user=request.user)
    except Despachador.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No tienes permisos de despachador."})

    viajes = Viaje.objects.select_related('conductor', 'origen').filter(asignador=despachador)
    return render(request, "conductor/ver_viajes.html", {"viajes": viajes})

# Vista despachador: ver estado global de todos los paquetes
@login_required
def ver_estado_global(request):
    try:
        Despachador.objects.get(user=request.user)
    except Despachador.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No tienes permisos de despachador."})

    paquetes = Paquete.objects.select_related('estado_actual', 'viaje', 'destino', 'destinatario')
    return render(request, "despachador/estado_global.html", {"paquetes": paquetes})

# Vista: registro de cliente
def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def home(request):
    """Simple home page view that requires login"""
    return render(request, 'home.html', {
        'user': request.user  # Pass the user object to the template
    })