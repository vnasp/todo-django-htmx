from django.db import migrations

def seed_data(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Task.objects.bulk_create([
        Task(title="Configurar entorno de trabajo", description="Instalar Django, Docker y preparar el proyecto base."),
        Task(title="Definir modelo Task", description="Crear estructura de datos para almacenar tareas."),
        Task(title="Cargar datos dummy", description="Revisar que se visualicen."),
        Task(title="Diseñar interfaz inicial", description="Implementar la vista principal con Tailwind y HTMX."),
        Task(title="Agregar interactividad", description="Permitir actualización dinámica sin recargar la página."),
        Task(title="Falta agregar la API", description="Implementar endpoints para operaciones CRUD."),
        Task(title="Opción C dashboard analítico", description="Integrar visualizaciones con Bokeh."),
        Task(title="Validar flujo de usuario", description="Probar tareas CRUD y navegación entre vistas."),
        Task(title="Crear README del proyecto", description="Registrar decisiones técnicas, trade-offs y puntos a mejorar."),
    ])

def unseed_data(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Task.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
