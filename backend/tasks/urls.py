from django.urls import path
from .views import TaskViewSet

urlpatterns = [
    path(
        "projects/<int:project_id>/tasks/",
        TaskViewSet.as_view({"get": "list", "post": "create"}),
        name="task-list",
    ),
    path(
        "projects/<int:project_id>/tasks/<int:pk>/",
        TaskViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="task-detail",
    ),
]
