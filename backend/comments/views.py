from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from tasks.models import Task
from workspaces.models import WorkspaceMembership

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task = get_object_or_404(
            Task,
            pk=self.kwargs["task_id"],
        )

        workspace = task.project.workspace

        get_object_or_404(
            WorkspaceMembership,
            workspace=workspace,
            user=self.request.user,
        )

        return Comment.objects.filter(task=task)

    def create(self, request):
        task = get_object_or_404(
            Task,
            pk=self.kwargs["task_id"],
        )

        workspace = task.project.workspace

        membership = get_object_or_404(
            WorkspaceMembership,
            workspace=workspace,
            user=request.user,
        )

        if membership.role == WorkspaceMembership.Role.VIEWER:
            raise PermissionDenied("Viewers cannot comment on tasks.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            task=task,
            author=request.user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        comment = self.get_object()

        task = comment.task
        workspace = task.project.workspace

        membership = get_object_or_404(
            WorkspaceMembership, workspace=workspace, user=request.user
        )

        if membership.role == WorkspaceMembership.Role.VIEWER:
            raise PermissionDenied("Viewers can not edit a comment.")

        if request.user != comment.author:
            raise PermissionDenied("You are not the author of this comment.")

        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save(is_edited=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        comment = self.get_object()
        task = comment.task
        workspace = task.project.workspace

        membership = get_object_or_404(
            WorkspaceMembership, workspace=workspace, user=request.user
        )

        if membership.role == WorkspaceMembership.Role.VIEWER:
            raise PermissionDenied("Viewers can not delete comment.")

        if request.user != comment.author:
            raise PermissionDenied("You are not the author of this comment.")

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
