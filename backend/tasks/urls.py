from django.urls import path
from .views import TaskListCreateAPIView, TaskRetrieveUpdateAPIView

urlpatterns = [
    path("", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("<int:id>/", TaskRetrieveUpdateAPIView.as_view(), name="task-retrieve-update"),
]
