from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

import requests

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


# Método auxiliar para hacer peticiones a la API interna
def call_internal_api(method, endpoint, data=None):
    """
    Realiza peticiones HTTP a la API REST interna.
    
    Args:
        method: Método HTTP (GET, POST, PUT, DELETE)
        endpoint: Endpoint de la API (ej: '/api/tasks/')
        data: Datos a enviar (opcional)
    
    Returns:
        Response object de requests
    """
    base_url = 'http://localhost:8000'
    url = f'{base_url}{endpoint}'
    
    headers = {'Content-Type': 'application/json'}
    
    if method.upper() == 'GET':
        return requests.get(url, headers=headers)
    elif method.upper() == 'POST':
        return requests.post(url, json=data, headers=headers)
    elif method.upper() == 'PUT':
        return requests.put(url, json=data, headers=headers)
    elif method.upper() == 'DELETE':
        return requests.delete(url, headers=headers)


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
    """Vista adaptadora que usa la API REST y devuelve HTML para HTMX"""
    def post(self, request, task_id):
        try:
            response = call_internal_api('POST', f'/api/tasks/{task_id}/toggle/')
            
            if response.status_code == 200:
                # Devolver las columnas actualizadas
                context = get_tasks_context()
                return render(request, 'partials/all_columns.html', context)
            else:
                # Manejar error de la API
                context = get_tasks_context()
                return render(request, 'partials/all_columns.html', context)
        except Exception as e:
            # Fallback en caso de error de conexión
            print(f"Error al llamar a la API: {e}")
            context = get_tasks_context()
            return render(request, 'partials/all_columns.html', context)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class APICreateTaskView(View):
    """Vista adaptadora que usa la API REST para crear tareas y devuelve HTML"""
    def post(self, request):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            try:
                data = {
                    'title': title,
                    'description': description
                }
                response = call_internal_api('POST', '/api/tasks/', data)
                
                if response.status_code not in [200, 201]:
                    print(f"Error al crear tarea: {response.status_code}")
            except Exception as e:
                print(f"Error al llamar a la API: {e}")
        
        # Devolver las columnas actualizadas
        context = get_tasks_context()
        return render(request, 'partials/all_columns.html', context)


@method_decorator(require_http_methods(["PUT", "POST"]), name='dispatch')
class APIUpdateTaskView(View):
    """Vista adaptadora que usa la API REST para actualizar tareas y devuelve HTML"""
    def post(self, request, task_id):
        return self.update(request, task_id)
    
    def put(self, request, task_id):
        return self.update(request, task_id)
    
    def update(self, request, task_id):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            # Llamar a la API REST para actualizar
            try:
                # Primero obtener la tarea actual para preservar otros campos
                task = get_object_or_404(Task, id=task_id)
                data = {
                    'title': title,
                    'description': description,
                    'completed': task.completed,
                    'deleted': task.deleted
                }
                response = call_internal_api('PUT', f'/api/tasks/{task_id}/', data)
                
                if response.status_code not in [200, 201]:
                    print(f"Error al actualizar tarea: {response.status_code}")
            except Exception as e:
                print(f"Error al llamar a la API: {e}")
        
        # Devolver las columnas actualizadas
        context = get_tasks_context()
        return render(request, 'partials/all_columns.html', context)


@method_decorator(require_http_methods(["DELETE", "POST"]), name='dispatch')
class APIDeleteTaskView(View):
    """Vista adaptadora que usa la API REST para soft-delete y devuelve HTML"""
    def delete(self, request, task_id):
        # Implementar soft-delete usando la API
        try:
            # Obtener la tarea actual
            task = get_object_or_404(Task, id=task_id)
            
            # Actualizar vía API marcando como deleted
            data = {
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'deleted': True  # Soft delete
            }
            response = call_internal_api('PUT', f'/api/tasks/{task_id}/', data)
            
            if response.status_code not in [200, 201]:
                print(f"Error al eliminar tarea: {response.status_code}")
        except Exception as e:
            print(f"Error al llamar a la API: {e}")
        
        # Devolver las columnas actualizadas
        context = get_tasks_context()
        return render(request, 'partials/all_columns.html', context)
    
    def post(self, request, task_id):
        return self.delete(request, task_id)

