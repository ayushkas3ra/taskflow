from rest_framework import serializers
from .models import Workspace, WorkspaceMembership

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "created_at", "updated_at"]
        

class WorkspaceInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=WorkspaceMembership.Role.choices)

    def validate_role(self, value):
        if value == WorkspaceMembership.Role.OWNER:
            raise serializers.ValidationError("You can not invite user as Owner")
        return value
    

class WorkspaceMembershipSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = WorkspaceMembership
        fields = ["id", "name", "role", "joined_at"]
        

class WorkspaceRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=WorkspaceMembership.Role.choices)


class WorkspaceTransferSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()