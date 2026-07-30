from rest_framework.viewsets import ModelViewSet
from .serializers import (
    WorkspaceSerializer,
    WorkspaceInviteSerializer,
    WorkspaceMembershipSerializer,
    WorkspaceRoleSerializer,
    WorkspaceTransferSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorkspaceOwner
from .models import Workspace, WorkspaceMembership
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceOwner]

    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            workspace = serializer.save(owner=self.request.user)

            WorkspaceMembership.objects.create(
                workspace=workspace,
                user=self.request.user,
                role=WorkspaceMembership.Role.OWNER,
            )

    @action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        serializer = WorkspaceInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace = self.get_object()
        data = serializer.validated_data
        email = data["email"]
        role = data["role"]
        user = get_object_or_404(User, email=email)

        if WorkspaceMembership.objects.filter(workspace=workspace, user=user).exists():
            return Response(
                {"error": "User is already a member"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            WorkspaceMembership.objects.create(
                workspace=workspace, user=user, role=role
            )
            return Response(
                {
                    "message": "User invited successfully",
                    "email": user.email,
                    "role": role,
                },
                status=status.HTTP_201_CREATED,
            )

    @action(detail=True, methods=["get"])
    def members(self, request, pk=None):
        workspace = self.get_object()
        members = WorkspaceMembership.objects.select_related("user").filter(
            workspace=workspace
        )
        serializer = WorkspaceMembershipSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path=r"members/(?P<member_id>[^/.]+)")
    def change_role(self, request, pk=None, member_id=None):
        workspace = self.get_object()
        membership = get_object_or_404(
            WorkspaceMembership, id=member_id, workspace=workspace
        )

        serializer = WorkspaceRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if membership.role == WorkspaceMembership.Role.OWNER:
            return Response(
                {
                    "error": "Owner role can only be changed through the transfer-owner endpoint"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.role = serializer.validated_data["role"]
        membership.save(update_fields=["role"])

        return Response(
            {
                "message": "Role updated successfully",
                "user": membership.user.email,
                "role": membership.role,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path=r"members/(?P<member_id>[^/.]+)")
    def remove_member(self, request, pk=None, member_id=None):
        workspace = self.get_object()
        membership = get_object_or_404(
            WorkspaceMembership, id=member_id, workspace=workspace
        )
        if membership.role == WorkspaceMembership.Role.OWNER:
            return Response(
                {"error": "Owner can not be deleted, transfer ownership first."}
            )
        # membership.is_active = False
        # membership.save(update_fields=["is_active"])
        membership.delete()
        return Response(
            {"message": "Member deleted successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], url_path="leave")
    def leave_workspace(self, request, pk=None):
        workspace = self.get_object()
        membership = get_object_or_404(
            WorkspaceMembership, workspace=workspace, user=request.user
        )
        if membership.role == WorkspaceMembership.Role.OWNER:
            return Response(
                {"error": "Owner can not leave workspace, transfer ownership first"},
                status=status.HTTP_403_FORBIDDEN,
            )
        membership.delete()
        return Response(
            {"message": "Left workspace successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"], url_path=r"transfer-owner")
    def transfer_owner(self, request, pk=None):
        serializer = WorkspaceTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member_id = serializer.validated_data["member_id"]

        workspace = self.get_object()

        new_owner_membership = get_object_or_404(
            WorkspaceMembership,
            id=member_id,
            workspace=workspace,
        )
        current_owner_membership = get_object_or_404(
            WorkspaceMembership, workspace=workspace, user=request.user
        )

        if new_owner_membership.user != WorkspaceMembership.Role.OWNER:
            return Response(
                {"error": "Only the owner can transfer ownership."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if new_owner_membership.user == request.user:
            return Response(
                {"message": "You can not transfer ownership to yourself"},
                status=status.HTTP_403_FORBIDDEN,
            )

        with transaction.atomic():
            current_owner_membership.role = WorkspaceMembership.Role.ADMIN
            new_owner_membership.role = WorkspaceMembership.Role.OWNER
            workspace.owner = new_owner_membership.user
            current_owner_membership.save()
            new_owner_membership.save()
            workspace.save()
        return Response(
            {"message": "Workspace ownership transferred successfully."},
            status=status.HTTP_200_OK,
        )
