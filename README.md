# Gestor de Tareas

Bienvenido al repositorio del Gestor de Tareas, un sitio web interactivo realizado con Django, HTMX, TailwindCSS donde podrás agregar, editar, completar y eliminar (o archivar) tareas, complementado con un dashboard de estadísticas utilizando la librería gráfica Bokeh.

## Instrucciones para correr el proyecto

Este proyecto se encuentra dockerizado para facilitar su desarrollo.

1. Construir y levantar el contenedor Docker

```bash
docker-compose up --build
```

2. Aplicar migraciones en otra pestaña terminal

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

3. Activa el watch de TailwindCSS

```bash
npm run dev:css
```

3. Acceder a la aplicación

- http://localhost:8000

## Características

- Interfaz tipo tablero con columnas Pendientes, Completadas, Eliminadas.
- Se pueden crear, editar, completar y eliminar (archivar) tareas.
- Interfaz reactiva sin recargar página gracias a HTMX.
- Diseño (no-responsive) con Tailwind CSS
- Dashboard estadístico con librería Bokeh
- API Rest con Django REST Framework que permite realizar CRUD sobre las tareas.

## Tecnologías utilizadas 💻

- **Backend**: Django 5.0, Django REST Framework 3.14
- **Gráficos**: Bokeh 3.3.0
- **Frontend**: HTMX 1.9.10 (CDN), Tailwind CSS 4.1.16 (instalado localmente)
- **Base de datos**: SQLite
- **Otros**: Docker, Python 3.12, Node.js

## Despliegue 🚀

Revisa la aplicación desplegada en Render: https://todo-django-htmx.onrender.com

Importante: El plan gratuito de Render demora unos segundos en levantar el despliegue.
