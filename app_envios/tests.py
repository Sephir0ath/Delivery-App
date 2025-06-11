from django.test import TestCase
from decimal import Decimal

# Create your tests here.
from django.urls import reverse

from app_envios.models import  Paquete, Viaje,  Sucursal
from app_autenticacion.models import Conductor, Usuario, Despachador, Cliente

class PedidosAsignadosTest(TestCase):
    def setUp(self):
        # Crear un usuario y su conductor
        self.usuario_asignador = Usuario.objects.create_user(username='asignador1', password='testing', tipo='despachador')
        self.asignador = Despachador.objects.create(user=self.usuario_asignador)
        self.usuario_conductor = Usuario.objects.create_user(username='conductor1', password='test1234', tipo='conductor')
        self.conductor = Conductor.objects.create(user=self.usuario_conductor)

        # Crear un destino y un viaje asociado a ese conductor
        self.origen = Sucursal.objects.create(comuna="Puerto Montt", latitud=Decimal('2.9'), longitud=Decimal('4.3'))
        self.destino = Sucursal.objects.create(comuna="Puerto Pinguino", latitud=Decimal('1.9'), longitud=Decimal('1.2'))
        self.viaje = Viaje.objects.create(asignador=self.asignador,conductor=self.conductor, origen=self.destino)

        self.usuario_cliente = Usuario.objects.create_user(username='cliente', password='pass', tipo='cliente')
        self.cliente = Cliente.objects.create(user=self.usuario_cliente)

        # Crear paquetes para este conductor
        for i in range(3):
            Paquete.objects.create(
                ancho = Decimal('5.0'),
                alto = Decimal('5.0'),
                largo = Decimal('5.0'),
                peso = Decimal('5.0'),
                viaje = self.viaje,
                destinatario = self.cliente,
                destino = self.destino,
            )

        # Crear otro usuario y otro paquete que NO debe aparecer
        self.usuario_asignador2 = Usuario.objects.create_user(username='otroasignador', password='testing', tipo='despachador')
        self.asignador2 = Despachador.objects.create(user=self.usuario_asignador2)
        self.usuario_otro = Usuario.objects.create_user(username='otro', password='test1234', tipo='conductor')
        self.otro_conductor = Conductor.objects.create(user=self.usuario_otro)

        self.origen2 = Sucursal.objects.create(comuna="Puerto Montt", latitud=Decimal('100.0'), longitud=Decimal('12.9'))
        self.destino2 = Sucursal.objects.create(comuna="Puerto Pinguino", latitud=Decimal('10.9'), longitud=Decimal('1.29'))
        self.viaje2 = Viaje.objects.create(asignador=self.asignador2,conductor=self.otro_conductor, origen=self.destino2)
        
        Paquete.objects.create(
                ancho = Decimal('5.0'),
                alto = Decimal('5.0'),
                largo = Decimal('5.0'),
                peso = Decimal('5.0'),
                viaje = self.viaje2,
                destinatario = self.cliente,
                destino = self.destino2,
        )

    def test_conductor_ve_solo_sus_pedidos(self):
        
        # Logueamos al conductor
        self.client.login(username='conductor1', password='test1234')
        
        # Accedemos a la vista
        response = self.client.get(reverse('mis_pedidos'))
        
        # Comprobamos que el código de estado sea 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Comprobamos que haya 3 paquetes (los suyos)
        self.assertContains(response, "Paquete 0")
        self.assertContains(response, "Paquete 1")
        self.assertContains(response, "Paquete 2")

        # Aseguramos que no aparece el paquete del otro conductor
        self.assertNotContains(response, "No debe aparecer")

    def test_no_logueado_redireccionado(self):
        response = self.client.get(reverse('mis_pedidos'))
        self.assertEqual(response.status_code, 302)  # Redirección al login
