from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from bokeh.plotting import figure
from bokeh.embed import components
import math
from .models import Task

class HomeClass(TemplateView):
    template_name = "home.html"

    def get_template_names(self):
        if self.request.htmx:
            return ["tasks.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_tasks"] = Task.objects.filter(completed=False, deleted=False).order_by("-created_at")
        context["completed_tasks"] = Task.objects.filter(completed=True, deleted=False).order_by("-created_at")
        context["deleted_tasks"] = Task.objects.filter(deleted=True).order_by("-created_at")
        return context


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class EditTaskFormView(View):
    """Vista para mostrar el formulario de edición inline"""
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'partials/edit_task_form.html', {'task': task})


def get_tasks_context():
    """
    Obtiene el contexto de tareas organizadas por estado.
    Consulta directamente el modelo para renderizar las vistas.
    """
    return {
        'pending_tasks': Task.objects.filter(completed=False, deleted=False).order_by("-created_at"),
        'completed_tasks': Task.objects.filter(completed=True, deleted=False).order_by("-created_at"),
        'deleted_tasks': Task.objects.filter(deleted=True).order_by("-created_at"),
    }


# Vistas adaptadoras para conectar API REST con HTMX
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class APIToggleTaskView(View):
    """Vista para alternar el estado de completado de una tarea"""
    def post(self, request, task_id):
        try:
            # Alternar el estado directamente en la base de datos
            task = get_object_or_404(Task, id=task_id)
            task.completed = not task.completed
            task.save()
        except Exception as e:
            print(f"Error al alternar tarea: {e}")
        
        # Devolver el contenedor completo de tareas
        context = get_tasks_context()
        return render(request, 'partials/tasks_container.html', context)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class APICreateTaskView(View):
    """Vista para crear tareas y devuelve HTML"""
    def post(self, request):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            try:
                # Crear directamente en la base de datos
                Task.objects.create(
                    title=title,
                    description=description
                )
            except Exception as e:
                print(f"Error al crear tarea: {e}")
        
        # Devolver el contenedor completo de tareas
        context = get_tasks_context()
        return render(request, 'partials/tasks_container.html', context)


@method_decorator(require_http_methods(["PUT", "POST"]), name='dispatch')
class APIUpdateTaskView(View):
    """Vista para actualizar tareas y devuelve HTML"""
    def post(self, request, task_id):
        return self.update(request, task_id)
    
    def put(self, request, task_id):
        return self.update(request, task_id)
    
    def update(self, request, task_id):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            # Actualizar directamente en la base de datos
            try:
                task = get_object_or_404(Task, id=task_id)
                task.title = title
                task.description = description
                task.save()
            except Exception as e:
                print(f"Error al actualizar tarea: {e}")
        
        # Devolver el contenedor completo de tareas
        context = get_tasks_context()
        return render(request, 'partials/tasks_container.html', context)


@method_decorator(require_http_methods(["DELETE", "POST"]), name='dispatch')
class APIDeleteTaskView(View):
    """Vista para soft-delete de tareas"""
    def delete(self, request, task_id):
        # Implementar soft-delete
        try:
            task = get_object_or_404(Task, id=task_id)
            task.deleted = True
            task.save()
        except Exception as e:
            print(f"Error al eliminar tarea: {e}")
        
        # Devolver el contenedor completo de tareas
        context = get_tasks_context()
        return render(request, 'partials/tasks_container.html', context)
    
    def post(self, request, task_id):
        return self.delete(request, task_id)


class DashboardView(TemplateView):

    def get_template_names(self):
        if self.request.htmx:
            return ["partials/dashboard_content.html"]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        total_tasks = Task.objects.count()
        pending_tasks = Task.objects.filter(completed=False, deleted=False).count()
        completed_tasks = Task.objects.filter(completed=True, deleted=False).count()
        deleted_tasks = Task.objects.filter(deleted=True).count()
        
        # Calcular porcentaje de completado respecto a tareas activas (sin eliminadas)
        active_tasks = pending_tasks + completed_tasks
        completion_rate = (completed_tasks / active_tasks * 100) if active_tasks > 0 else 0
        
        context.update({
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'deleted_tasks': deleted_tasks,
            'completion_rate': round(completion_rate, 1),
        })
        
        # Gráfico tipo pie
        if total_tasks > 0:
            data = {
                'status': ['Pendientes', 'Completadas', 'Eliminadas'],
                'count': [pending_tasks, completed_tasks, deleted_tasks],
                'color': ['#EAB308', '#22C55E', '#EF4444']
            }
            
            angles = []
            for count in data['count']:
                angle = (count / total_tasks) * 2 * math.pi
                angles.append(angle)
            
            pie_chart = figure(
                width=500,
                height=400,
                title="Distribución de Tareas por Estado",
                toolbar_location=None,
                tools="hover",
                tooltips="@status: @count",
                x_range=(-0.5, 1.0)
            )
            
            start_angle = 0
            for i, (status, count, color, angle) in enumerate(zip(data['status'], data['count'], data['color'], angles)):
                if count > 0:
                    pie_chart.wedge(
                        x=0, y=1,
                        radius=0.4,
                        start_angle=start_angle,
                        end_angle=start_angle + angle,
                        color=color,
                        alpha=0.8,
                        legend_label=f"{status}: {count}"
                    )
                    start_angle += angle
            
            pie_chart.axis.axis_label = None
            pie_chart.axis.visible = False
            pie_chart.grid.grid_line_color = None
            pie_chart.legend.location = "top_right"
            
            script_pie, div_pie = components(pie_chart)
            context['script_pie'] = script_pie
            context['div_pie'] = div_pie
        else:
            context['script_pie'] = ''
            context['div_pie'] = '<p class="text-center text-gray-500">No hay datos para mostrar</p>'
        
        # Gráfico de barras
        bar_chart = figure(
            x_range=['Pendientes', 'Completadas', 'Eliminadas'],
            width=500,
            height=400,
            title="Comparación de Tareas por Estado",
            toolbar_location=None,
            tools=""
        )
        
        bar_chart.vbar(
            x=['Pendientes', 'Completadas', 'Eliminadas'],
            top=[pending_tasks, completed_tasks, deleted_tasks],
            width=0.6,
            color=['#EAB308', '#22C55E', '#EF4444'],
            alpha=0.8
        )
        
        bar_chart.xgrid.grid_line_color = None
        bar_chart.y_range.start = 0
        bar_chart.yaxis.axis_label = "Cantidad de Tareas"
        
        script_bar, div_bar = components(bar_chart)
        context['script_bar'] = script_bar
        context['div_bar'] = div_bar
        
        return context