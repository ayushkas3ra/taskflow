from django.db import models
from workspaces.models import Workspace

class Project(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    due_date = models.DateField(blank = True, null = True)
    workspace = models.ForeignKey(
        Workspace,
        on_delete = models.CASCADE,
        related_name = "projects"
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["workspace", "name"],
                name = "unique_project_name_per_workspace"
            )
        ]
        
    def __str__(self):
        return self.name