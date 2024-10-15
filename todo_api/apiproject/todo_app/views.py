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
from todo_app.pagination import TodoCursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

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
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)