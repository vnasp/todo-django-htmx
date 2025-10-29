# Gestor de Tareas

Este proyecto es un gestor de tareas realizado con Django, HTMX, TailwindCSS, Bokeh, en un ambiente de contenedor Docker, bajo un tiempo limitado de desarrollo.

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

3. Acceder a la aplicación

- http://localhost:8000

## Características

- Interfaz tipo tablero con columnas Pendientes, Completadas, Eliminadas.
- Se pueden crear, editar, completar y eliminar (archivar) tareas.
- Interfaz reactiva sin recargar página gracias a HTMX.
- Diseño (no-responsive) con Tailwind CSS
- Dashboard estadístico con librería Bokeh
- API Rest con Django REST Framework que permite realizar CRUD sobre las tareas.

## Tecnologías utilizadas

- **Backend**: Django 5.0, Django REST Framework 3.14
- **Gráficos**: Bokeh 3.3.0
- **Frontend**: HTMX 1.9.10 (CDN), Tailwind CSS (CDN)
- **Base de datos**: SQLite
- **Otros**: Docker, Python 3.12

## Decisiones técnicas

- Docker porque permite mantener el mismo entorno entre distintos desarrolladores.
- TailwindCSS desde CDN, aunque lo ideal sería instalarlo para aprovechar funciones como @apply y crear un tema propio.
- Agregué dos campos al modelo: updated_at, para controlar cuándo se edita una tarea y soft_deleted, para simular un eliminado visual y mostrar esas tareas en una columna separada, tipo Trello.
- Elegí desarrollar la opción de Dashboard porque es el tipo de trabajo con el que estoy más familiarizada. Actualmente realizo visualizaciones y paneles de datos complejos con Bokeh, por lo que me resultó natural aplicar esa experiencia aquí.

## Trade-offs

- Priorizé el uso de CDN de Tailwind en lugar de una configuración más completa con instalación local y componentes personalizados, para poder desarrollar y lanzar más rápido, siguiendo una lógica lean.

- Aunque tengo una orientación marcada hacia la usabilidad y la experiencia del usuario, en esta ocasión decidí dejar de lado algunos detalles visuales para poder cumplir con uno de los opcionales que aportara mayor valor al proyecto.

- Tuve que aplicar prettier-ignore en algunos archivos debido a mi configuración actual en VSCode, que rompía una sintaxis del template de Django (los bloques {% %} y {{ }}). Con más tiempo, habría ajustado la configuración del editor para evitar ese conflicto.

## Puntos a mejorar

- Mejoraría la parte visual (UI/UX) instalando TailwindCSS, usando una nomenclatura como BEM (para facilitar mantenimiento) y por supuesto que fuese responsive.
- Además de los tests unitarios básicos, incorporaría una herramienta como Playwright para realizar tests e2e porque esta app es altamente interactiva y se beneficiaría de pruebas que validen la experiencia del usuario.
