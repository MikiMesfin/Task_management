from django.core.management.base import BaseCommand
from django.utils import timezone
from task.models import Task

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        tasks = Task.objects.filter(status='completed', recurring__in=['daily', 'weekly'])
        for task in tasks:
            next_due_date = task.regenerate()
            if next_due_date:
                Task.objects.create(
                    title=task.title,
                    description=task.description,
                    due_date=next_due_date,
                    priority=task.priority,
                    user=task.user,
                    recurring=task.recurring,
                )
