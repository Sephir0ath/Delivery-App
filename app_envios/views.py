from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from app_envios.models import Conductor, Paquete, Sucursal, Despachador, Viaje

@login_required
def pedidos_asignados_conductor(request):
    # Paso 1: Obtener el conductor actual usando el usuario logueado
    try:
        conductor = Conductor.objects.get(user=request.user)
    except Conductor.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No eres un conductor registrado."})

    # Paso 2: Obtener todos los paquetes cuyo viaje fue asignado al conductor
    paquetes = Paquete.objects.select_related(
        'viaje', 'destino', 'destinatario'
    ).filter(
        viaje__conductor=conductor
    )

    # Paso 3: Renderizar una plantilla con los paquetes
    return render(request, "conductor/paquetes_asignados.html", {"paquetes": paquetes})
# Create your views here.

@login_required
def asignar_paquetes(request):
    # Verificar si el usuario es un despachador
    try:
        despachador = Despachador.objects.get(user=request.user)
    except Despachador.DoesNotExist:
        return render(request, "error.html", {"mensaje": "No tienes permisos de despachador."})

    if request.method == 'POST':
        # Obtener datos del formulario
        conductor_id = request.POST.get('conductor')
        sucursal_id = request.POST.get('sucursal')
        paquetes_ids = request.POST.getlist('paquetes')
        
        # Validar selección
        if not conductor_id or not sucursal_id or not paquetes_ids:
            return render(request, "error.html", {"mensaje": "Debes seleccionar un conductor, una sucursal y al menos un paquete."})
        
        try:
            # Obtener objetos de la base de datos
            conductor = Conductor.objects.get(id=conductor_id, disponible=True)
            sucursal = Sucursal.objects.get(id=sucursal_id)
            paquetes = Paquete.objects.filter(id__in=paquetes_ids, viaje__isnull=True)
            
            # Verificar que haya paquetes válidos
            if not paquetes.exists():
                return render(request, "error.html", {"mensaje": "Los paquetes seleccionados ya están asignados o no existen."})
            
            # Crear viaje y asignar paquetes (transacción atómica)
            with transaction.atomic():
                viaje = Viaje.objects.create(
                    asignador=despachador,
                    conductor=conductor,
                    origen=sucursal
                )
                paquetes.update(viaje=viaje)
                
            return redirect('asignar_paquetes')
            
        except (Conductor.DoesNotExist, Sucursal.DoesNotExist):
            return render(request, "error.html", {"mensaje": "Selección inválida. Intenta nuevamente."})
    
    # GET request: Mostrar formulario
    paquetes_sin_asignar = Paquete.objects.filter(viaje__isnull=True).select_related('destinatario', 'destino')
    conductores_disponibles = Conductor.objects.filter(disponible=True).select_related('user')
    sucursales = Sucursal.objects.all()
    
    return render(request, "despachador/asignar_paquetes.html", {
        'paquetes': paquetes_sin_asignar,
        'conductores': conductores_disponibles,
        'sucursales': sucursales
    })