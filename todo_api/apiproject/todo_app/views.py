from django.shortcuts import render
from todo_app.models import TodoList
from todo_app.serializers import TodoListSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from todo_app.permissions import IsOwner
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from todo_app.pagination import TodoListPagination, TodoLOPagination, TodoCursorPagination


class TodoListAPIView(generics.ListCreateAPIView):
    serializer_class = TodoListSerializers
    filter_backends = [DjangoFilterBackend]
    pagination_class = TodoCursorPagination

    def get_queryset(self):
        """
        Optionally restricts the returned todo items to the given user,
        by filtering against a `user` query parameter in the URL.
        """
        return TodoList.objects.filter(user=self.request.user)
        # return TodoList.objects.all()
    
    def perform_create(self, serializer):
        # Only save the user if they are authenticated
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)  # Automatically set the user
        else:
            raise serializer.ValidationError("You must be logged in to create a todo item.")


# class TodoListAPIView(APIView):

#     def get(self, request):
#         # todolist = TodoList.objects.filter(user = request.user)
#         todolist = TodoList.objects.all()
#         serializer = TodoListSerializers(todolist, many=True)

#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = TodoListSerializers(data = request.data)

#         if serializer.is_valid():
#             serializer.save(user = request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TodoListUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializers
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj) 
        return obj
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    


# class TodoListUpdate(APIView):

#     permission_classes = [IsOwner]

#     def get(self, request, pk):
#         todo_item = get_object_or_404(TodoList, pk=pk)
#         self.check_object_permissions(request, todo_item)
       
#         # if not request.user == todo_item.user:
#         #     return Response({"error": "You do not have permission to view this item."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = TodoListSerializers(todo_item)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         todo_item = get_object_or_404(TodoList, pk=pk)
#         self.check_object_permissions(request, todo_item)
        
#         # if not request.user == todo_item.user:
#         #     return Response({"error": "You do not have permission to edit this item."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = TodoListSerializers(todo_item, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         todo_item = get_object_or_404(TodoList, pk=pk)
#         self.check_object_permissions(request, todo_item)

#         # if not request.user == todo_item.user:
#         #     return Response({"error": "You do not have permission to edit this item."}, status=status.HTTP_403_FORBIDDEN)

#         todo_item.delete()
#         return Response({'message': 'Todo item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class TodoStatusUpdate(APIView):

    permission_classes = [IsOwner]

    def patch(self, request, pk):
        todo_item = get_object_or_404(TodoList, pk=pk)
        self.check_object_permissions(request, todo_item)

        if todo_item.status == 'To Do':
            todo_item.status = 'Done'
        else:
            todo_item.status = 'To Do'

        todo_item.save()

        serializer = TodoListSerializers(todo_item)
        return Response(serializer.data, status=status.HTTP_200_OK)