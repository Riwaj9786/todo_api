from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class TodoList(models.Model):

    Status_Choices = {
        "Done": "Done",
        "To Do": "To Do"
    }

    def get_deadline():
        return timezone.now() + timedelta(hours=24)

    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=200, null=True, blank=True)
    deadline = models.DateTimeField(default=get_deadline, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status_Choices)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_user')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_id()

        super(TodoList, self).save(*args, **kwargs)
    

    def generate_id(self):
        last_todo = TodoList.objects.order_by('created').last()

        if last_todo:
            last_id = int(last_todo.id.split('_')[1])
            new_id = last_id + 1
        else:
            new_id = 1
            
        return f"TID_{new_id:06d}"
    
    def __str__(self):
        return f"{self.id}-{self.title}"