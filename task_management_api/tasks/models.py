from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Task(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    ]

    PENDING = 'Pending'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def save(self, *args, **kwargs):
        if self.status == self.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()
        if self.status == self.PENDING:
            self.completed_at = None
        if self.due_date < timezone.now().date():
            raise ValueError("Due date cannot be in the past.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def clean(self):
      if self.due_date < timezone.now().date():
        raise ValidationError('Due date must be in the future.')

