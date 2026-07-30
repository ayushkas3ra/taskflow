from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_workspaces",
    )

    def __str__(self):
        return self.name


class WorkspaceMembership(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workspace_memberships"
    )
    joined_at = models.DateField(auto_now_add=True)

    class Role(models.TextChoices):
        OWNER = "OW", _("Owner")
        MEMBER = "ME", _("Member")
        ADMIN = "AD", _("Admin")
        VIEWER = "VI", _("Viewer")

    role = models.CharField(max_length=2, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "user"], name="unique_workspace_member"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.role}"
