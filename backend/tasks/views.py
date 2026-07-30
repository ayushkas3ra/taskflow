from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from projects.models import Project
from workspaces.models import WorkspaceMembership
from .serializers import TaskSerializer

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "is_finished",
        "project",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "name",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Task.objects.select_related(
                "project",
                "project__workspace",
            )
            .filter(project__workspace__memberships__user=self.request.user)
            .distinct()
        )

    def get_project(self):
        return get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace__memberships__user=self.request.user,
        )

    def get_membership(self, project):
        return get_object_or_404(
            WorkspaceMembership, workspace=project.workspace, user=self.request.user
        )

    def check_can_modify(self, membership):
        if membership.role == WorkspaceMembership.Role.VIEWER:
            raise PermissionDenied("Viewers cannot modify tasks.")

    # def perform_create(self, serializer):
    #     project = self.get_project()
    #     membership = self.get_membership(project)

    #     self.check_can_modify(membership)
    #     serializer.save(project=project)

    def perform_create(self, serializer):
        print("project_id:", self.kwargs["project_id"])

        project = self.get_project()
        print("Project found:", project)

        membership = self.get_membership(project)
        print("Membership found:", membership)

        self.check_can_modify(membership)
        serializer.save(project=project)

    def perform_update(self, serializer):
        project = serializer.instance.project
        membership = self.get_membership(project)
        self.check_can_modify(membership)
        serializer.save()

    def perform_destroy(self, instance):
        project = instance.project
        membership = self.get_membership(project)
        self.check_can_modify(membership)
        instance.delete()
