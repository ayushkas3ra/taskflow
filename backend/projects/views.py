from .serializers import ProjectSerializer
from .models import Project
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            workspace_id=self.kwargs["workspace_id"], workspace__owner=self.request.user
        )

    def perform_create(self, serializer):
        workspace = get_object_or_404(
            Workspace, id=self.kwargs["workspace_id"], owner=self.request.user
        )
        serializer.save(workspace=workspace)
        