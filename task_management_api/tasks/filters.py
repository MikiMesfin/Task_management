from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = filters.ChoiceFilter(choices=Task.PRIORITY_LEVELS)
    due_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date']
