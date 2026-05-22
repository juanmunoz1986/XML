import os
from django.core.management.base import BaseCommand
from activos.models import ActivoTecnico

class Command(BaseCommand):
    """
    Comando de administración personalizado de Django para poblar la base de datos.
    Se ejecuta desde la terminal con: python manage.py seed_activos
    Esto es de gran valor didáctico ya que muestra cómo automatizar tareas en Django.
    """
    
    # Mensaje de ayuda que se muestra al ejecutar 'python manage.py seed_activos --help'
    help = 'Pobla la base de datos con activos técnicos de prueba para demostración.'

    def handle(self, *args, **options):
        # 1. Mensaje de inicio de proceso
        self.stdout.write(self.style.WARNING("Iniciando la siembra de datos (seeding)..."))

        # 2. Definimos una lista de diccionarios con los datos de prueba
        datos_prueba = [
            {
                "nombre": "Laptop Lenovo ThinkPad L14",
                "cantidad": 10,
                "valor_unitario": 850.00
            },
            {
                "nombre": "Monitor Dell 27' UltraSharp",
                "cantidad": 15,
                "valor_unitario": 320.00
            },
            {
                "nombre": "Servidor Dell PowerEdge R750",
                "cantidad": 2,
                "valor_unitario": 4500.00
            },
            {
                "nombre": "Router Cisco ISR 4331",
                "cantidad": 5,
                "valor_unitario": 1150.00
            },
            {
                "nombre": "Switch Switchboard Cisco 24 Puertos POE",
                "cantidad": 8,
                "valor_unitario": 650.00
            }
        ]

        # 3. Iteramos e insertamos en la BD evitando duplicados usando get_or_create
        # get_or_create busca si ya existe un registro con el 'nombre' dado.
        # Si existe, lo devuelve; si no, lo crea con los valores adicionales (defaults).
        contador_creados = 0
        for item in datos_prueba:
            activo, creado = ActivoTecnico.objects.get_or_create(
                nombre=item["nombre"],
                defaults={
                    "cantidad": item["cantidad"],
                    "valor_unitario": item["valor_unitario"]
                }
            )
            
            if creado:
                contador_creados += 1
                self.stdout.write(self.style.SUCCESS(f"Creado: {activo.nombre}"))
            else:
                self.stdout.write(self.style.WARNING(f"Ya existía: {activo.nombre}"))

        # 4. Mensaje final indicando el resultado
        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso finalizado. Se crearon {contador_creados} nuevos activos técnicos."
            )
        )
