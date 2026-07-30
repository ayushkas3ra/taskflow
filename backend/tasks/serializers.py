from rest_framework import serializers
from .models import Task

from projects.serializers import ProjectSerializer


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    def validate_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Task name must be atleast 5 characters long."
            )
        return value

    def create(self, validated_data):
        if not validated_data.get("description"):
            validated_data["description"] = "No description available for this task"
        return Task.objects.create(**validated_data)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "is_finished",
            "project",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "project",
            "created_at",
            "updated_at",
        ]
