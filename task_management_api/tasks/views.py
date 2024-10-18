from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task
from .models import Category
from .serializers import TaskSerializer, RegisterSerializer, UserSerializer
from .serializers import CategorySerializer
from rest_framework.decorators import api_view, permission_classes

# List View for Tasks (Retrieve all tasks for the authenticated user)
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']  # Add fields for filtering
    ordering_fields = ['due_date', 'priority']  # Add fields for sorting
    ordering = ['due_date']  # Default ordering by due_date

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# Create View for Tasks
class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Add the request to the context
        return context


# Update View for Tasks
class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user) | Task.objects.filter(shared_with=self.request.user)

# Delete View for Tasks
class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only delete their own tasks
        return Task.objects.filter(user=self.request.user)

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskCreateTemplateView(APIView):
    template_name = 'tasks/task_form.html'

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, context={'request': request})  # Pass request in context
        if serializer.is_valid():
            serializer.save(user=request.user)  # Ensure user is saved correctly
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateTemplateView(TemplateView):
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(pk=self.kwargs['pk'])
        context['form'] = TaskSerializer(instance=task)
        return context

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        serializer = TaskSerializer(instance=task, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('task-list')
        return self.get_context_data(form=serializer)

class TaskDeleteTemplateView(TemplateView):
    template_name = 'tasks/task_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        task.delete()
        return redirect('task-list')

class TaskDetailView(TemplateView):
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs['pk']  # Get the task ID from the URL
        context['task'] = Task.objects.get(id=task_id, user=self.request.user)  # Get the task for the logged-in user
        return context

class TaskHistoryView(TemplateView):
    template_name = 'tasks/task_history.html'  # Adjust to your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you want to filter completed tasks for the user
        context['completed_tasks'] = Task.objects.filter(user=self.request.user, status='completed')  # Adjust 'status' as necessary
        return context

class HomePageView(TemplateView):
    template_name = 'home.html'

class APIHomeView(TemplateView):
    template_name = 'api_home.html'

class CategoryListView(TemplateView):
    template_name = 'categories/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Adjust if filtering by user
        return context

class CategoryCreateTemplateView(TemplateView):
    template_name = 'categories/category_form.html'

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('category-list')
        return self.get_context_data(form=serializer)

class CategoryUpdateTemplateView(TemplateView):
    template_name = 'categories/category_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['form'] = CategorySerializer(instance=category)
        return context

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])
        serializer = CategorySerializer(instance=category, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('category-list')
        return self.get_context_data(form=serializer)

class CategoryDeleteTemplateView(TemplateView):
    template_name = 'categories/category_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])
        category.delete()
        return redirect('category-list')

class CategoryTemplateView(TemplateView):
    template_name = 'categories/category_list.html'  # Adjust according to your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)  # Assuming categories are user-specific
        return context

class TaskHistoryView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, status='completed')

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

