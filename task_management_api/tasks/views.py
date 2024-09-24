from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


# Create your views here.

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCompleteView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = Task.COMPLETED if task.status == Task.PENDING else Task.PENDING
        task.save()
        return Response(TaskSerializer(task).data)
