from rest_framework import serializers
from .models import Project

from workspaces.serializers import WorkspaceSerializer

class ProjectSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer(read_only = True)
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "due_date",
            "workspace",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "workspace",
            "created_at",
            "updated_at"
        ]