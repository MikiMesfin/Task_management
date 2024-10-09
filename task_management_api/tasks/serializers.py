from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'user']
        read_only_fields = ['id', 'completed_at', 'user']  # Ensure user and completion timestamp are read-only

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Set the user to the currently authenticated user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('status') == 'completed' and instance.completed_at is None:
            instance.completed_at = timezone.now()
        elif validated_data.get('status') == 'pending':
            instance.completed_at = None  # Reset timestamp if reverted to pending
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


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def validate(self, data):
        # Check if all fields are provided
        if not data.get('username'):
            raise serializers.ValidationError({"username": "This field is required."})
        if not data.get('password'):
            raise serializers.ValidationError({"password": "This field is required."})
        if not data.get('email'):
            raise serializers.ValidationError({"email": "This field is required."})
        return data

    def create(self, validated_data):
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user