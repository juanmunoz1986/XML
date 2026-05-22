from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from activos.models import ActivoTecnico

class ActivoTecnicoIntegrationTests(TestCase):
    def setUp(self):
        # El framework de pruebas de Django limpia la base de datos automáticamente
        pass

    def test_flujo_completo_activo_y_xml(self):
        # 1. Crear un activo técnico (POST)
        url_crear = reverse('crear_activo')
        datos_creacion = {
            'nombre': 'Prueba Servidor Cloud',
            'cantidad': 4,
            'valor_unitario': '1500.00'
        }
        response = self.client.post(url_crear, datos_creacion)
        # Redirecciona al dashboard en caso de éxito
        self.assertEqual(response.status_code, 302)

        # Verificar en base de datos
        activo = ActivoTecnico.objects.filter(nombre='Prueba Servidor Cloud').first()
        self.assertIsNotNone(activo)
        self.assertEqual(activo.cantidad, 4)
        self.assertEqual(activo.valor_unitario, Decimal('1500.00'))
        self.assertEqual(activo.subtotal, Decimal('6000.00'))

        # 2. Leer Dashboard (GET)
        url_dashboard = reverse('dashboard')
        response = self.client.get(url_dashboard)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prueba Servidor Cloud')

        # 3. Modificar el activo (POST)
        url_editar = reverse('editar_activo', kwargs={'pk': activo.id})
        datos_edicion = {
            'nombre': 'Prueba Servidor Cloud Modificado',
            'cantidad': 5,
            'valor_unitario': '1400.00'
        }
        response = self.client.post(url_editar, datos_edicion)
        self.assertEqual(response.status_code, 302)

        activo.refresh_from_db()
        self.assertEqual(activo.nombre, 'Prueba Servidor Cloud Modificado')
        self.assertEqual(activo.cantidad, 5)
        self.assertEqual(activo.valor_unitario, Decimal('1400.00'))
        self.assertEqual(activo.subtotal, Decimal('7000.00'))

        # 4. Crear un segundo activo para probar reportes XML
        # Total Global esperado = 7000 (Activo 1) + 3000 (Activo 2) = 10000.00
        ActivoTecnico.objects.create(
            nombre='Switch de Fibra Optica',
            cantidad=5,
            valor_unitario=Decimal('600.00')
        )

        # Descargar XML (GET)
        url_descargar_xml = reverse('descargar_xml')
        response = self.client.get(url_descargar_xml)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])

        xml_content = response.content.decode('utf-8')
        # Validar estructura matemática del XML generado
        self.assertIn('<total_global>10000.00</total_global>', xml_content)
        self.assertIn('<cantidad_total_equipos>10</cantidad_total_equipos>', xml_content)
        self.assertIn('<subtotal>7000.00</subtotal>', xml_content)
        self.assertIn('<porcentaje_del_total>70.00</porcentaje_del_total>', xml_content)
        self.assertIn('<subtotal>3000.00</subtotal>', xml_content)
        self.assertIn('<porcentaje_del_total>30.00</porcentaje_del_total>', xml_content)

        # 5. Eliminar el activo técnico (POST)
        url_eliminar = reverse('eliminar_activo', kwargs={'pk': activo.id})
        response = self.client.post(url_eliminar)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ActivoTecnico.objects.filter(id=activo.id).exists())

