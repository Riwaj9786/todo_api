from django.shortcuts import render
from todo_app.models import TodoList
from todo_app.serializers import TodoListSerializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from todo_app.permissions import IsOwner
from rest_framework import status


class TodoListAPIView(APIView):

    permission_classes = [IsOwner]

    def get(self, request):
        todolist = TodoList.objects.filter(user = request.user)
        serializer = TodoListSerializers(todolist, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = TodoListSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
