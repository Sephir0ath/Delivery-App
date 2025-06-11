# views.py
import requests
from django.shortcuts import render, get_object_or_404
from app_envios.models import Viaje, Sucursal
from django.conf import settings  # API Key desde settings

def optimizar_ruta(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)

    # Obtener sucursales únicas asociadas a los paquetes del viaje
    sucursales = Sucursal.objects.filter(paquete__viaje=viaje).distinct()
    coordenadas = [(s.longitud, s.latitud) for s in sucursales]

    if len(coordenadas) <= 1:
        return render(request, 'error.html', {'mensaje': 'Se necesita más de una sucursal para optimizar.'})

    # Armar los datos para ORS
    jobs = [{"id": i + 1, "location": coord} for i, coord in enumerate(coordenadas)]

    data = {
        "jobs": jobs,
        "vehicles": [{
            "id": 1,
            "profile": "driving-car",
            "start": coordenadas[0],
            "end": coordenadas[0],
        }]
    }

    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.openrouteservice.org/optimization", json=data, headers=headers)
    result = response.json()

    orden_ids = [step["id"] for step in result["routes"][0]["steps"] if step["type"] == "job"]
    orden_sucursales = [sucursales[i - 1] for i in orden_ids]

    # Guardar orden como lista de IDs de sucursales en el viaje
    viaje.orden_sucursales = [s.id for s in orden_sucursales]
    viaje.save()

    return render(request, 'ruta_mapa.html', {
        'sucursales': [
            {'lat': s.latitud, 'lon': s.longitud} for s in orden_sucursales
        ]
    })



