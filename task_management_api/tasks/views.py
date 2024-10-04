from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User




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

# User Registration View
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    
@api_view(['POST'])
def mark_task_complete(request, pk):
    task = Task.objects.filter(pk=pk, user=request.user).first()
    if task:
        task.status = 'Completed'
        task.save()
        return Response({'status': 'Task marked as complete'}, status=status.HTTP_200_OK)
    return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def mark_task_incomplete(request, pk):
    task = Task.objects.filter(pk=pk, user=request.user).first()
    if task:
        task.status = 'Pending'
        task.save()
        return Response({'status': 'Task reverted to incomplete'}, status=status.HTTP_200_OK)
    return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public access to this endpoint
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    return Response({'success': 'User registered successfully.'}, status=status.HTTP_201_CREATED)