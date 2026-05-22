import xml.etree.ElementTree as ET
from xml.dom import minidom
from django.utils.timezone import now
from decimal import Decimal

def generar_xml_activos(activos_queryset):
    """
    Función de Lógica de Negocio que toma un conjunto de datos (QuerySet)
    de Activos Técnicos de la base de datos y genera un reporte estructurado en XML.
    
    Aplica las fórmulas:
      - Subtotal de un ítem = Cantidad * Valor Unitario
      - Total Global = Sumatoria de los Subtotales de todos los ítems
      - Porcentaje = (Subtotal del Ítem / Total Global) * 100
      
    Retorna una tupla: (xml_string_bonito, xml_bytes)
    """
    
    # 1. CÁLCULO DE MÉTRICAS GLOBALES (Paso previo para calcular porcentajes)
    # Sumamos el subtotal de cada activo en memoria.
    # Usamos Decimal para mantener la precisión decimal y evitar errores de redondeo de punto flotante.
    total_global = Decimal('0.00')
    cantidad_total_equipos = 0
    
    for activo in activos_queryset:
        total_global += activo.subtotal
        cantidad_total_equipos += activo.cantidad

    # 2. CREACIÓN DEL ÁRBOL XML CON ELEMENTTREE
    # Creamos el nodo raíz del XML: <reporte_activos>
    # Incluimos un atributo 'fecha_generacion' usando la zona horaria del servidor.
    raiz = ET.Element('reporte_activos')
    raiz.set('fecha_generacion', now().strftime('%Y-%m-%d %H:%M:%S'))

    # Creamos un contenedor intermedio para agrupar los activos: <activos>
    nodo_activos = ET.SubElement(raiz, 'activos')

    # 3. LLENADO DE CADA ACTIVO Y CÁLCULOS MATEMÁTICOS INDIVIDUALES
    for activo in activos_queryset:
        # Se crea el nodo hijo: <activo id="X">
        # El atributo 'id' debe ser una cadena (convertimos el entero de la BD)
        nodo_activo = ET.SubElement(nodo_activos, 'activo')
        nodo_activo.set('id', str(activo.id))

        # Subnodo Nombre: <nombre>Texto</nombre>
        nombre_elem = ET.SubElement(nodo_activo, 'nombre')
        nombre_elem.text = activo.nombre

        # Subnodo Cantidad: <cantidad>Número</cantidad>
        cantidad_elem = ET.SubElement(nodo_activo, 'cantidad')
        cantidad_elem.text = str(activo.cantidad)

        # Subnodo Valor Unitario: <valor_unitario>Monto</valor_unitario>
        valor_uni_elem = ET.SubElement(nodo_activo, 'valor_unitario')
        valor_uni_elem.text = f"{activo.valor_unitario:.2f}"

        # Subnodo Subtotal (Cantidad * Valor Unitario)
        # Se calcula mediante la propiedad @property que definimos en el modelo
        subtotal_elem = ET.SubElement(nodo_activo, 'subtotal')
        subtotal_elem.text = f"{activo.subtotal:.2f}"

        # Subnodo Porcentaje de representación sobre el costo total de todos los activos
        # Fórmula: Porcentaje = (Subtotal / Total Global) * 100
        # Validamos que el total_global no sea cero para evitar la excepción ZeroDivisionError.
        if total_global > 0:
            porcentaje = (activo.subtotal / total_global) * Decimal('100.00')
        else:
            porcentaje = Decimal('0.00')

        porcentaje_elem = ET.SubElement(nodo_activo, 'porcentaje_del_total')
        # Formateamos a 2 decimales f-string
        porcentaje_elem.text = f"{porcentaje:.2f}"

    # 4. CREACIÓN DEL NODO DE RESUMEN (Punto crítico del requerimiento)
    # Este nodo consolidará los datos del inventario de forma global.
    nodo_resumen = ET.SubElement(raiz, 'resumen')

    # Subnodo Total Global: <total_global>Monto total</total_global>
    total_global_elem = ET.SubElement(nodo_resumen, 'total_global')
    total_global_elem.text = f"{total_global:.2f}"

    # Subnodo Cantidad Total de Equipos: <cantidad_total_equipos>Suma cantidades</cantidad_total_equipos>
    cant_total_elem = ET.SubElement(nodo_resumen, 'cantidad_total_equipos')
    cant_total_elem.text = str(cantidad_total_equipos)

    # 5. GENERACIÓN Y FORMATEO DEL XML ("PRETTY PRINTING")
    # Convertimos el árbol XML de ElementTree a una cadena de bytes con codificación UTF-8
    xml_bruto = ET.tostring(raiz, encoding='utf-8')

    # Usamos la librería minidom de Python para reformatear e indentar el XML,
    # haciendo que sea fácilmente legible en pantalla para un humano.
    xml_parseado = minidom.parseString(xml_bruto)
    # toprettyxml genera una cadena de texto (str) con sangrías (\t o espacios) y saltos de línea
    xml_bonito = xml_parseado.toprettyxml(indent="  ")

    # También generamos una versión en bytes limpia para la descarga directa del archivo.
    # Al pasar la codificación a toprettyxml() obtenemos una respuesta en bytes (utf-8).
    xml_bytes_descarga = xml_parseado.toprettyxml(indent="  ", encoding="utf-8")

    return xml_bonito, xml_bytes_descarga
