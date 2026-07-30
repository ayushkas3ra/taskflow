from django.db import models
from projects.models import Project


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_finished = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"], name="unique_task_name_per_project"
            )
        ]

    def __str__(self):
        return self.name
