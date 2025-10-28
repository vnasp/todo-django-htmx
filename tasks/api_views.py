from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
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
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """
        Endpoint personalizado para alternar el estado de completado de una tarea.
        POST /api/tasks/{id}/toggle/
        """
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
