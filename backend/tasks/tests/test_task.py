from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from workspaces.models import Workspace, WorkspaceMembership
from projects.models import Project
from tasks.models import Task
from django.urls import reverse

User = get_user_model()


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="raunak",
            email="ayush@example.com",
            password="password123",
            first_name="Raunak",
            last_name="Singh",
        )

        self.workspace = Workspace.objects.create(
            name="office", description="office-workspace description", owner=self.user
        )

        self.membership = WorkspaceMembership.objects.create(
            workspace=self.workspace,
            user=self.user,
            role=WorkspaceMembership.Role.OWNER,
        )

        self.project = Project.objects.create(
            name="office-project", workspace=self.workspace
        )

    def test_owner_can_create_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list", kwargs={"project_id": self.project.id})
        response = self.client.post(
            url,
            {
                "name": "Implement login",
                "description": "Create JWT authentication",
                "due_date": "2026-08-15",
            },
            format="json",
        )
        task = Task.objects.first()

        self.assertEqual(task.name, "Implement login")
        self.assertEqual(task.project, self.project)
        self.assertEqual(response.status_code, 201)
