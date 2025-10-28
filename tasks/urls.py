from django.urls import path
from .views import HomeClass, AddTaskView, EditTaskFormView, UpdateTaskView, ToggleTaskView, DeleteTaskView

urlpatterns = [
    path("", HomeClass.as_view(), name="home"),
    path("add-task/", AddTaskView.as_view(), name="add_task"),
    path("edit-task/<int:task_id>/", EditTaskFormView.as_view(), name="edit_task"),
    path("update-task/<int:task_id>/", UpdateTaskView.as_view(), name="update_task"),
    path("toggle-task/<int:task_id>/", ToggleTaskView.as_view(), name="toggle_task"),
    path("delete-task/<int:task_id>/", DeleteTaskView.as_view(), name="delete_task"),
]
