from django.urls import path
from todo_app import views

app_name = 'todo_app'

urlpatterns = [
    path("", views.TodoListAPIView.as_view(), name="todo-list"),
    path('<pk>/', views.TodoListUpdate.as_view(), name="todo_update"),

    # Endpoint to change the status of the todo_item
    path('<pk>/status/', views.TodoStatusUpdate.as_view(), name="status_update"),
]