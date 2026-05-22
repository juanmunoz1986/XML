from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import ActivoTecnico
from .utils import generar_xml_activos
from decimal import Decimal

def dashboard(request):
    """
    Vista principal que actúa como el Dashboard de la aplicación.
    Muestra la lista de todos los activos en una tabla, calcula estadísticas generales,
    y opcionalmente genera e inserta el XML formateado para visualización directa.
    """
    # 1. Recuperamos todos los activos de la base de datos.
    # Gracias a la Meta clase en el modelo, se ordenan automáticamente por ID descendente.
    activos = ActivoTecnico.objects.all()

    # 2. Calculamos estadísticas rápidas para adornar la interfaz (KPIs)
    # Sumamos cantidades y valores totales para las tarjetas de información.
    total_inversion = sum(activo.subtotal for activo in activos)
    cantidad_total = sum(activo.cantidad for activo in activos)
    total_equipos_distintos = activos.count()

    # 3. Comprobamos si el usuario solicitó ver el reporte XML en pantalla.
    # Esto ocurre cuando se presiona el botón "Generar Informe XML", que recarga la página
    # añadiendo el parámetro '?ver_xml=1' en la URL.
    xml_reporte = None
    if 'ver_xml' in request.GET:
        if activos.exists():
            # Invocamos la función de lógica de negocio en utils.py
            # Esta función devuelve una tupla, tomamos el primer valor (la cadena formateada)
            xml_reporte, _ = generar_xml_activos(activos)
            messages.success(request, "Reporte XML generado con éxito en el visor.")
        else:
            messages.warning(request, "No hay activos registrados en la base de datos para generar el XML.")

    # 4. Definimos el contexto con los datos que se enviarán a la plantilla HTML.
    context = {
        'activos': activos,
        'total_inversion': total_inversion,
        'cantidad_total': cantidad_total,
        'total_equipos_distintos': total_equipos_distintos,
        'xml_reporte': xml_reporte,
    }

    # 5. Renderizamos la plantilla dashboard.html enviando el contexto.
    return render(request, 'activos/dashboard.html', context)


def crear_activo(request):
    """
    Vista para crear un nuevo Activo Técnico.
    Maneja la petición POST enviada desde el modal de la página principal.
    """
    if request.method == 'POST':
        # Extracción de los datos del formulario POST
        nombre = request.POST.get('nombre')
        cantidad_raw = request.POST.get('cantidad')
        valor_unitario_raw = request.POST.get('valor_unitario')

        # Validación básica en el servidor
        try:
            cantidad = int(cantidad_raw)
            valor_unitario = Decimal(valor_unitario_raw)

            if cantidad <= 0 or valor_unitario <= 0:
                raise ValueError("La cantidad y el valor unitario deben ser mayores a cero.")

            # Crear y guardar el nuevo registro en la base de datos usando el ORM
            activo = ActivoTecnico.objects.create(
                nombre=nombre,
                cantidad=cantidad,
                valor_unitario=valor_unitario
            )
            # Sistema de notificaciones flash de Django
            messages.success(request, f"El activo '{activo.nombre}' fue registrado con éxito.")
        
        except (ValueError, TypeError) as e:
            messages.error(request, f"Error al registrar el activo: {str(e)}")

    # Redirecciona a la vista del dashboard para recargar la tabla principal
    return redirect('dashboard')


def editar_activo(request, pk):
    """
    Vista para actualizar un activo técnico existente por su Clave Primaria (ID).
    Recibe la petición POST enviada desde el modal de edición.
    """
    # get_object_or_404 busca el objeto en la BD. Si no existe, devuelve una respuesta HTTP 404 (Not Found).
    activo = get_object_or_404(ActivoTecnico, pk=pk)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad_raw = request.POST.get('cantidad')
        valor_unitario_raw = request.POST.get('valor_unitario')

        try:
            cantidad = int(cantidad_raw)
            valor_unitario = Decimal(valor_unitario_raw)

            if cantidad <= 0 or valor_unitario <= 0:
                raise ValueError("Los valores numéricos deben ser mayores a cero.")

            # Modificamos los atributos del objeto recuperado
            activo.nombre = nombre
            activo.cantidad = cantidad
            activo.valor_unitario = valor_unitario
            
            # Guardamos los cambios en la BD. El ORM genera un SQL UPDATE en el fondo.
            activo.save()
            messages.success(request, f"El activo '{activo.nombre}' fue actualizado correctamente.")
        
        except (ValueError, TypeError) as e:
            messages.error(request, f"Error al actualizar el activo: {str(e)}")

    return redirect('dashboard')


def eliminar_activo(request, pk):
    """
    Vista para eliminar un activo técnico de la base de datos.
    Se utiliza POST por seguridad, evitando eliminaciones por GET accidentales.
    """
    activo = get_object_or_404(ActivoTecnico, pk=pk)
    
    if request.method == 'POST':
        nombre_activo = activo.nombre
        # El ORM ejecuta un SQL DELETE sobre el registro
        activo.delete()
        messages.success(request, f"El activo '{nombre_activo}' fue eliminado del inventario.")
    
    return redirect('dashboard')


def descargar_xml(request):
    """
    Vista que genera el reporte XML y lo descarga directamente
    como un archivo adjunto ('reporte_activos.xml') en el navegador.
    """
    activos = ActivoTecnico.objects.all()
    
    if not activos.exists():
        messages.error(request, "No hay activos disponibles para generar el reporte.")
        return redirect('dashboard')

    # Generamos la data binaria del XML
    _, xml_bytes = generar_xml_activos(activos)

    # Creamos una HttpResponse con el contenido binario del XML.
    # Especificamos el tipo MIME 'application/xml' para indicarle al navegador de qué tipo de archivo se trata.
    response = HttpResponse(xml_bytes, content_type='application/xml')
    
    # Añadimos la cabecera 'Content-Disposition' para forzar la descarga del archivo con un nombre predefinido.
    response['Content-Disposition'] = 'attachment; filename="reporte_activos.xml"'
    
    return response


def ver_xml_crudo(request):
    """
    Vista técnica que genera el reporte XML y lo muestra directamente en el navegador
    en formato plano/crudo (MIME type application/xml). Excelente para comprobar
    el árbol XML nativamente en el navegador.
    """
    activos = ActivoTecnico.objects.all()
    
    if not activos.exists():
        return HttpResponse("Error: No hay activos registrados para generar el XML.", content_type="text/plain; charset=utf-8")

    # Obtenemos el string XML formateado y lo codificamos a bytes utf-8 para la salida
    xml_bonito, _ = generar_xml_activos(activos)
    
    return HttpResponse(xml_bonito, content_type='application/xml; charset=utf-8')
