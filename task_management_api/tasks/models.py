from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use AUTH_USER_MODEL

    def __str__(self):
        return self.name


def validate_due_date(value):
    if value < timezone.now():
        raise ValidationError('Due date must be in the future.')


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    RECURRING_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(validators=[validate_due_date])
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)  # Timestamp for completion
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Each task is tied to a user
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Optional category
    recurring = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_tasks', blank=True)

    def clean(self):
        # Compare due_date with timezone.now() to avoid datetime vs date comparison
        if self.due_date < timezone.now():
            raise ValidationError("Due date must be in the future.")

    def save(self, *args, **kwargs):
        if self.status == 'completed' and self.completed_at is None:
            self.completed_at = timezone.now()
        elif self.status == 'pending':
            self.completed_at = None  # Reset timestamp if reverted to pending
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Task: {self.title}, Status: {self.status}, Due: {self.due_date}"

    def regenerate(self):
        if self.recurring == 'daily':
            return timezone.now() + timezone.timedelta(days=1)
        elif self.recurring == 'weekly':
            return timezone.now() + timezone.timedelta(weeks=1)
        return None


class CustomUser(AbstractUser):
    class Meta:
        app_label = 'tasks'
        swappable = 'AUTH_USER_MODEL'

    # Add any custom fields you need
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
