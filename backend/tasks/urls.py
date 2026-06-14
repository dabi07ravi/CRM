from django.urls import path
from .views import TaskCreateView, TaskListView, MyTaskListView, TaskDetailView, TaskAssignView, TaskStatusUpdateView, TaskDeleteView



urlpatterns = [
    path("create/", TaskCreateView.as_view(), name="create_task"),
    path("", TaskListView.as_view(), name = 'list_tasks'),
    path("my_tasks/", MyTaskListView.as_view(), name = 'my_tasks'),
    path("<int:id>/", TaskDetailView.as_view(), name = 'get_task'),
    path(
    "<int:id>/assign/",
    TaskAssignView.as_view(),
    name="task_assign"),
    path(
    "<int:id>/status/",
    TaskStatusUpdateView.as_view(),
    name="task_status"),
    path(
    "delete/<int:id>/",
    TaskDeleteView.as_view(),
    name="task_del"),
]