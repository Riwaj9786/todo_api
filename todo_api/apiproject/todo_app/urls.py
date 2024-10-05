from django.urls import path
from todo_app.views import TodoListAPIView

app_name = 'todo_app'

urlpatterns = [
    path("", TodoListAPIView.as_view(), name="todo_list"),
]