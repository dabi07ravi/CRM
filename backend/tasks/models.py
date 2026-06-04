from django.db import models

from django.conf import settings

from .choices import TaskStatus

class Task(models.Model):

    title = models.CharField(max_length=255)    
    description = models.TextField()
    assigned_to = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="assigned_tasks"

    )
    assigned_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="created_tasks"

    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title