from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Task, Category
from django.contrib.auth import get_user_model

class TaskTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        url = reverse('task-create')
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': '2024-12-31T00:00:00Z',
            'priority': 'medium'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_update_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            priority="medium"
        )
        url = reverse('task-update', kwargs={'pk': task.pk})
        data = {'title': 'Updated Task'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(pk=task.pk).title, 'Updated Task')
