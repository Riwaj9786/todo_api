from rest_framework import serializers
from todo_app.models import TodoList

class TodoListSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = TodoList
        fields = ['id', 'title', 'description', 'created', 'deadline', 'status', 'username']
        read_only_fields = ['id', 'created', 'username'] 