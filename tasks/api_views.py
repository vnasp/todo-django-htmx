from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Gestión de tareas (sin endpoint de detalle individual).
    
    Endpoints disponibles:
    - GET /api/tasks/ - Listar todas las tareas
    - POST /api/tasks/ - Crear nueva tarea
    - PUT /api/tasks/{id}/ - Actualizar tarea completa
    - DELETE /api/tasks/{id}/ - Eliminar tarea
    - POST /api/tasks/{id}/toggle/ - Alternar estado completado
    """
    queryset = Task.objects.all().order_by('created_at')
    serializer_class = TaskSerializer
    
    def get_response_for_htmx(self):
        """Retorna HTML renderizado para peticiones HTMX"""
        pending_tasks = Task.objects.filter(completed=False, deleted=False).order_by("-created_at")
        completed_tasks = Task.objects.filter(completed=True, deleted=False).order_by("-created_at")
        deleted_tasks = Task.objects.filter(deleted=True).order_by("-created_at")
        
        context = {
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'deleted_tasks': deleted_tasks,
        }
        html = render_to_string('partials/all_columns.html', context)
        return HttpResponse(html, content_type='text/html')
    
    def create(self, request, *args, **kwargs):
        """POST - Crear tarea"""
        response = super().create(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            return self.get_response_for_htmx()
        return response
    
    def update(self, request, *args, **kwargs):
        """PUT - Actualizar tarea"""
        response = super().update(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            return self.get_response_for_htmx()
        return response
    
    def destroy(self, request, *args, **kwargs):
        """DELETE - Eliminar tarea"""
        response = super().destroy(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            return self.get_response_for_htmx()
        return response
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """
        Endpoint personalizado para alternar el estado de completado de una tarea.
        POST /api/tasks/{id}/toggle/
        """
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        if request.headers.get('HX-Request'):
            return self.get_response_for_htmx()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
