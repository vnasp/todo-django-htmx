from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
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


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AddTaskView(View):
    def post(self, request):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            task = Task.objects.create(title=title, description=description)
        
        context = {
            'pending_tasks': Task.objects.filter(completed=False, deleted=False).order_by("-created_at"),
            'completed_tasks': Task.objects.filter(completed=True, deleted=False).order_by("-created_at"),
            'deleted_tasks': Task.objects.filter(deleted=True).order_by("-created_at"),
        }
        return render(request, 'partials/all_columns.html', context)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class EditTaskFormView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'partials/edit_task_form.html', {'task': task})


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class UpdateTaskView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            task.title = title
            task.description = description
            task.save()
        
        context = {
            'pending_tasks': Task.objects.filter(completed=False, deleted=False).order_by("-created_at"),
            'completed_tasks': Task.objects.filter(completed=True, deleted=False).order_by("-created_at"),
            'deleted_tasks': Task.objects.filter(deleted=True).order_by("-created_at"),
        }
        return render(request, 'partials/all_columns.html', context)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class ToggleTaskView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed
        task.save()
        
        context = {
            'pending_tasks': Task.objects.filter(completed=False, deleted=False).order_by("-created_at"),
            'completed_tasks': Task.objects.filter(completed=True, deleted=False).order_by("-created_at"),
            'deleted_tasks': Task.objects.filter(deleted=True).order_by("-created_at"),
        }
        return render(request, 'partials/all_columns.html', context)


@method_decorator(require_http_methods(["DELETE", "POST"]), name='dispatch')
class DeleteTaskView(View):
    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.deleted = True  # Simula archivado
        task.save()
        
        context = {
            'pending_tasks': Task.objects.filter(completed=False, deleted=False).order_by("-created_at"),
            'completed_tasks': Task.objects.filter(completed=True, deleted=False).order_by("-created_at"),
            'deleted_tasks': Task.objects.filter(deleted=True).order_by("-created_at"),
        }
        return render(request, 'partials/all_columns.html', context)
    
    def post(self, request, task_id):
        return self.delete(request, task_id)
