from rest_framework import serializers
from todo_app.models import TodoList

class TodoListSerializers(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ['id', 'title', 'description', 'deadline', 'status', 'user']
        read_only_fields = ['id', 'created_at', 'user'] 