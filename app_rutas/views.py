# views.py
import requests
from django.shortcuts import render, get_object_or_404
from app_envios.models import Viaje, Sucursal
from django.conf import settings  # API Key desde settings

def optimizar_ruta(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)
    
    # Get unique branches
    sucursales = Sucursal.objects.filter(paquete__viaje=viaje).distinct()
    coordenadas = [[s.longitud, s.latitud] for s in sucursales]  # Note: using list instead of tuple

    if len(coordenadas) <= 1:
        return render(request, 'error.html', {'mensaje': 'Se necesita más de una sucursal para optimizar.'})

    # Optimization request
    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        # 1. Get optimized order
        opt_data = {
            "jobs": [{"id": i+1, "location": coord} for i, coord in enumerate(coordenadas)],
            "vehicles": [{
                "id": 1,
                "profile": "driving-car",
                "start": coordenadas[0],
                "end": coordenadas[0],
            }]
        }
        
        opt_response = requests.post(
            "https://api.openrouteservice.org/optimization", 
            json=opt_data, 
            headers=headers
        )
        opt_response.raise_for_status()
        opt_result = opt_response.json()

        # Get ordered coordinates
        orden_ids = [step["id"] for step in opt_result["routes"][0]["steps"] if step["type"] == "job"]
        orden_coordenadas = [coordenadas[i-1] for i in orden_ids]

        # 2. Get route geometry
        dir_data = {
            "coordinates": orden_coordenadas,
            "geometry": "true",
            "instructions": "false"
        }

        dir_response = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car/geojson",
            json=dir_data,
            headers=headers
        )
        dir_response.raise_for_status()
        dir_result = dir_response.json()

        # Prepare context
        context = {
            'sucursales': [{'lat': coord[1], 'lon': coord[0]} for coord in orden_coordenadas],
            'route_geometry': dir_result['features'][0]['geometry']['coordinates'],
            'debug_data': {
                'optimization': opt_result,
                'directions': dir_result
            }
        }

        # Save order
        orden_sucursales = [sucursales[i-1] for i in orden_ids]
        viaje.orden_sucursales = [s.id for s in orden_sucursales]
        viaje.save()

        return render(request, 'ruta_mapa.html', context)

    except Exception as e:
        return render(request, 'error.html', {
            'mensaje': f"Error al calcular la ruta: {str(e)}",
            'debug': {
                'coordenadas': coordenadas,
                'error': str(e)
            }
        })