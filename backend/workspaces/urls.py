from django.urls import path
from .views import WorkspaceViewSet

urlpatterns = [
    path("workspaces/", WorkspaceViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "workspaces/<int:pk>/",
        WorkspaceViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
