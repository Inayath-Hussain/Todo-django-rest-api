from rest_framework import serializers
from .models import TodoItem


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'title', 'description', 'due_date', 'status', 'user']
