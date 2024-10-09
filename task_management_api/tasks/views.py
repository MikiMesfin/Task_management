from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes

# List View for Tasks (Retrieve all tasks for the authenticated user)
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the tasks that belong to the logged-in user
        return Task.objects.filter(user=self.request.user)


# Create View for Tasks
class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


# Update View for Tasks
class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only update their own tasks
        return Task.objects.filter(user=self.request.user)


# Delete View for Tasks
class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only delete their own tasks
        return Task.objects.filter(user=self.request.user)


# User Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user (authenticated or not) to access this view

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the new user
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
