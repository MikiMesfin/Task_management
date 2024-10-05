from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'user']

    def validate_status(self, value):
        """Ensure that once a task is completed, it cannot be edited unless reverted to incomplete."""
        instance = self.instance
        if instance and instance.status == Task.COMPLETED and value == Task.PENDING:
            raise serializers.ValidationError("You cannot revert a completed task to incomplete status.")
        return value

    def update(self, instance, validated_data):
        if validated_data.get('status') == Task.COMPLETED and instance.status != Task.COMPLETED:
            instance.completed_at = timezone.now()
        elif validated_data.get('status') == Task.PENDING:
            instance.completed_at = None  # Reset completed timestamp if reverted to pending
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')