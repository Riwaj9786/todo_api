from django.urls import path
from todo_app.views import TodoListAPIView, TodoListUpdate, TodoStatusUpdate

app_name = 'todo_app'

urlpatterns = [
    path("", TodoListAPIView.as_view(), name="todo_list"),
    path('<pk>/', TodoListUpdate.as_view(), name="todo_update"),

    # Endpoint to change the status of the todo_item
    path('<pk>/status/', TodoStatusUpdate.as_view(), name="status_update"),
]