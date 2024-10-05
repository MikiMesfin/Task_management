from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)  # Timestamp for completion
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each task is tied to a user

    def clean(self):
        if self.due_date < timezone.now():
            raise ValidationError("Due date must be in the future.")

    def save(self, *args, **kwargs):
        if self.status == 'completed' and self.completed_at is None:
            self.completed_at = timezone.now()
        elif self.status == 'pending':
            self.completed_at = None  # Reset timestamp if reverted to pending
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
