from django.urls import path
from .views import CommentViewSet

urlpatterns = [
    path(
        "tasks/<int:task_id>/comments/",
        CommentViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="task-comments",
    ),
    path(
        "comments/<int:pk>/",
        CommentViewSet.as_view(
            {
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comment-detail",
    ),
]
