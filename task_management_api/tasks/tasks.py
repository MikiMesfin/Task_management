from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
from .views import CategoryListView

def send_reminder_emails():
    tasks = Task.objects.filter(due_date__lte=timezone.now() + timezone.timedelta(days=1), status='pending')
    for task in tasks:
        send_mail(
            'Task Due Reminder',
            f'Remember to complete your task: {task.title}',
            'from@example.com',
            [task.user.email],
        )
