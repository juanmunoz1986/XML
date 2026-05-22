# Gestión de Activos Técnicos con Reportes XML en Django 🚀

Este proyecto es una aplicación web educativa desarrollada en **Django** para la materia **"Aplicaciones y Tendencias"** (8vo Semestre). El sistema implementa un flujo completo de gestión de inventario (**CRUD**) para activos técnicos y cuenta con un motor especializado que procesa datos de inventario y los compila en reportes técnicos estructurados en formato **XML**.

---

## 📋 Características Principales

* **CRUD Completo:** Permite Registrar, Visualizar, Editar y Eliminar activos técnicos del inventario desde una misma vista sin recargas molestas, utilizando ventanas emergentes (Modales de Bootstrap 5).
* **Cálculos Financieros Robustos:** Los montos y porcentajes se gestionan a través de la librería `Decimal` de Python para evitar errores de redondeo asociados a números de punto flotante (`float`).
* **Generación de XML Orgánica:** Construcción de reportes XML jerárquicos a través del módulo estándar `xml.etree.ElementTree`.
* **Cálculo de Porcentaje y Consolidación (Punto Crítico):** Cada activo en el XML detalla su subtotal y el porcentaje exacto de representación económica sobre el total del inventario. Incluye un nodo `<resumen>` con la sumatoria total del costo y la cantidad global de equipos.
* **Descarga e Inserción XML:** El XML se puede visualizar formateado con colores de código directamente en el navegador, descargar como archivo físico `.xml` o ver en su formato plano crudo.
* **Diseño Web Premium:** Interfaz responsive inspirada en sistemas SaaS modernos usando Bootstrap 5, iconos vectoriales, y efectos de micro-animaciones (hover effects).

---

## 🛠️ Arquitectura y Flujo del Sistema

La aplicación sigue el patrón de diseño clásico de Django **MVT (Model-View-Template)**, expandiendo la capa de controlador con un módulo de generación XML de lógica de negocio:

```
  [ Cliente (Navegador) ] 
       ▲            │ (Petición HTTP GET / POST)
       │            ▼
  [ Vista Django (views.py) ] 
       ▲            │ (Consulta ORM)
       │            ▼
  [ Modelo (models.py) ]  ◀───▶  [ Base de Datos (SQLite) ]
       │
       ▼ (Envía QuerySet de Activos)
  [ Generador XML (utils.py) ]
       │ (Cálculos de Totales y Porcentajes)
       ▼
  [ Retorna XML a la Vista ] ───▶ [ Renderizado final en Cliente ]
```

---

## 📂 Estructura del Proyecto

A continuación se detalla la organización de los archivos principales creados en el espacio de trabajo:

```text
XML/
│
├── manage.py                     # Script de entrada para comandos de Django
├── core/                         # Configuración central del proyecto
│   ├── settings.py               # Registro de apps, idioma en español, zona horaria y hosts
│   └── urls.py                   # Enrutador principal del proyecto
│
└── activos/                      # Aplicación local "activos"
    ├── management/
    │   └── commands/
    │       └── seed_activos.py   # Comando personalizado para poblar datos de prueba
    ├── migrations/               # Historial de versiones de base de datos
    ├── models.py                 # Definición de la entidad ActivoTecnico y subtotal
    ├── utils.py                  # Lógica matemática y parseo a árbol XML (ElementTree)
    ├── views.py                  # Controladores para CRUD, descarga y visualización de XML
    ├── urls.py                   # Rutas de navegación de la app
    └── templates/
        └── activos/
            ├── base.html         # Plantilla HTML base (CDN de Bootstrap, estilos y fuentes)
            └── dashboard.html    # Panel de control, modales CRUD y visor de código XML
```

---

## 🧮 Fórmulas Matemáticas Utilizadas

1. **Subtotal por Ítem:**
   $$Subtotal = Cantidad \times Valor Unitario$$
2. **Total Global del Inventario:**
   $$Total Global = \sum_{i=1}^{n} Subtotal_i$$
3. **Porcentaje de Participación Económica:**
   $$Porcentaje = \left( \frac{Subtotal_i}{Total Global} \right) \times 100$$
   *(Redondeado estrictamente a 2 decimales para precisión en el XML)*

---

## 🚀 Guía de Instalación y Ejecución Local

Sigue estos pasos detallados para levantar el proyecto en tu máquina local:

### 1. Clonar o descargar el proyecto
Asegúrate de extraer el código en una carpeta de trabajo (ej. `C:\Users\tu_usuario\Escritorio\XML`).

### 2. Crear y activar el Entorno Virtual (Recomendado)
Abre tu terminal (PowerShell o CMD) en la raíz del proyecto y ejecuta:
```powershell
# Crear entorno virtual llamado .venv
python -m venv .venv

# Activar el entorno virtual en Windows (PowerShell)
.venv\Scripts\Activate.ps1

# O en Windows (CMD)
.venv\Scripts\activate.bat
```

### 3. Instalar Django
Con el entorno virtual activo (aparecerá `(.venv)` a la izquierda de la consola), instala Django:
```powershell
pip install django
```

### 4. Crear la Base de Datos y aplicar Migraciones
Crea las tablas locales en SQLite utilizando el ORM de Django:
```powershell
python manage.py migrate
```

### 5. Sembrar Datos de Prueba (Seeding)
Para no iniciar con un dashboard vacío, ejecuta el comando personalizado que poblará la base de datos con activos de prueba:
```powershell
python manage.py seed_activos
```

### 6. Ejecutar el Servidor local
Arranca el servidor web de desarrollo:
```powershell
python manage.py runserver
```

Abre tu navegador de preferencia e ingresa a: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## ☁️ Guía Rápida de Despliegue en la Nube (Render)

1. Genera el archivo de dependencias en la raíz del proyecto:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```
2. Asegúrate de que `ALLOWED_HOSTS = ['*']` en `core/settings.py`.
3. Sube el código a un repositorio público en **GitHub** (el archivo `.gitignore` ya está preconfigurado para omitir archivos locales como `.venv` y `db.sqlite3`).
4. Ve a **Render.com**, crea un nuevo **Web Service** y conéctalo a tu repositorio.
5. Usa los siguientes parámetros en la configuración:
   * **Environment:** `Python`
   * **Build Command:** `pip install -r requirements.txt && python manage.py migrate`
   * **Start Command:** `gunicorn core.wsgi:application`

---

## 🎓 Material de Sustentación para Evaluaciones

En caso de que el docente realice preguntas técnicas durante la defensa del proyecto, consulta la guía didáctica creada en la raíz de tu proyecto:
👉 **[walkthrough.md](file:///C:/Users/juano/.gemini/antigravity/brain/2b6601e1-89cb-43c3-be23-02e2e5cbced9/walkthrough.md)** (contiene preguntas frecuentes, diagramas y justificación del uso de librerías).
