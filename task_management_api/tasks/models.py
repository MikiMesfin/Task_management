from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each category belongs to a user

    def __str__(self):
        return self.name

def validate_due_date(value):
    if value < timezone.now().date():
        raise ValidationError('Due date must be in the future.')


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each task is tied to a user
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Optional category
    recurring = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')
    shared_with = models.ManyToManyField(User, related_name='shared_tasks', blank=True)



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
        return f"Task: {self.title}, Status: {self.status}, Due: {self.due_date}"


    def regenerate(self):
        if self.recurring == 'daily':
            return timezone.now() + timezone.timedelta(days=1)
        elif self.recurring == 'weekly':
            return timezone.now() + timezone.timedelta(weeks=1)
        return None

    def __str__(self):
        return self.title





