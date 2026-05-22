from django.db import models

# Definición del modelo "ActivoTecnico"
# Un modelo en Django representa una tabla en la base de datos relacional.
# Cada atributo de la clase se mapea a una columna de la tabla.
class ActivoTecnico(models.Model):
    """
    Clase que representa un Activo Técnico en el inventario.
    Al heredar de models.Model, Django automáticamente le crea un campo ID autoincremental
    como clave primaria (Primary Key), que actúa como identificador único de cada registro.
    """
    
    # Campo para almacenar el nombre del equipo técnico.
    # Se utiliza CharField para cadenas de texto de longitud limitada.
    # max_length define el límite de caracteres en la base de datos (buenas prácticas de optimización).
    nombre = models.CharField(
        max_length=150, 
        verbose_name="Nombre del equipo"
    )
    
    # Campo para almacenar la cantidad de equipos de este tipo en inventario.
    # PositiveIntegerField restringe los valores a enteros no negativos en la base de datos.
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad"
    )
    
    # Campo para el costo unitario del activo técnico.
    # DecimalField es ideal para datos financieros o de costos porque evita los errores de redondeo de punto flotante.
    # max_digits=12: permite almacenar números de hasta 12 dígitos en total (ej. 9999999999.99).
    # decimal_places=2: reserva exactamente dos posiciones para los decimales (centavos).
    valor_unitario = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Valor Unitario"
    )

    # Método especial __str__ (método mágico de Python)
    # Define cómo se representará el objeto cuando se convierta a una cadena de texto (ej. en el panel de administración).
    def __str__(self):
        return f"{self.nombre} (Cantidad: {self.cantidad})"

    # Decorador @property para definir un método que se comporta como un atributo de lectura.
    # Permite obtener el subtotal (cantidad * valor unitario) dinámicamente sin guardarlo en la base de datos.
    # Esto evita la redundancia de datos (Tercera Forma Normal - 3FN en base de datos).
    @property
    def subtotal(self):
        """
        Calcula el costo total del activo multiplicando su cantidad por el valor unitario.
        Retorna un tipo Decimal que mantiene la precisión financiera.
        """
        return self.cantidad * self.valor_unitario

    # Configuración adicional del modelo usando una clase interna Meta
    class Meta:
        verbose_name = "Activo Técnico"
        verbose_name_plural = "Activos Técnicos"
        # Ordenar por defecto de manera descendente por el ID (los más recientes primero)
        ordering = ['-id']
