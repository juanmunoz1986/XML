from django.urls import path
from . import views

# Definimos las rutas (endpoints) específicas de la aplicación "activos".
# Cada ruta asocia un patrón de URL con una función del archivo views.py.
# El parámetro 'name' permite realizar enrutamiento inverso (usar nombres en lugar de rutas duras en el HTML).
urlpatterns = [
    # Ruta principal: Muestra el listado de activos y el visor XML
    path('', views.dashboard, name='dashboard'),
    
    # Rutas para el CRUD de Activos Técnicos
    path('crear/', views.crear_activo, name='crear_activo'),
    # <int:pk> es un convertidor de ruta de Django.
    # Especifica que el parámetro debe ser un entero y se pasará a la vista con el nombre 'pk' (Primary Key).
    path('editar/<int:pk>/', views.editar_activo, name='editar_activo'),
    path('eliminar/<int:pk>/', views.eliminar_activo, name='eliminar_activo'),
    
    # Rutas para la gestión e informes XML
    path('reporte/descargar/', views.descargar_xml, name='descargar_xml'),
    path('reporte/ver/', views.ver_xml_crudo, name='ver_xml_crudo'),
]
