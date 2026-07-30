from django.urls import path
from .views import ProjectViewSet

urlpatterns = [
    path(
        "workspaces/<int:workspace_id>/projects/",
        ProjectViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "workspaces/<int:workspace_id>/projects/<int:pk>/",
        ProjectViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
