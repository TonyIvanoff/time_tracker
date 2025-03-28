from django.db import models
import uuid


class Task(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    task_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    task_duration = models.DurationField(blank=True, null=True)
    task_comment = models.CharField(max_length=1000, blank=True, null=True)
    

    PRODUCTION = 'p'
    NON_PRODUCTION = 'n'

    TASK_TYPE = [
        (PRODUCTION, 'Production'),
        (NON_PRODUCTION, 'Non-production'),
    ]

    type = models.CharField(max_length=1, choices=TASK_TYPE, blank=True, default=PRODUCTION)

    WAITING = 'w'
    STARTED = 's'
    PAUSED = 'p'
    COMPLETED = 'c'

    TASK_STATUS = [
        (WAITING, 'Waiting'),
        (STARTED, 'Started'),
        (PAUSED, 'Paused'),
        (COMPLETED, 'Completed'),
    ]

    status = models.CharField(max_length=1, choices=TASK_STATUS, blank=True, default=WAITING)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        

        if self.task_comment:
            Comment.objects.create(task=self, comment=self.task_comment)
            self.task_comment = ""

        if self.closed_at:
            if self.closed_at > self.created_at:
                self.task_duration = self.closed_at - self.created_at
            else:
                self.closed_at = None
                self.task_duration = None

        super(Task, self).save(*args, **kwargs)  # Save Task again to update task_duration

    def __str__(self):
        return f"Task {self.task_id} - {self.get_status_display()}"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.task:
            return f"Comment on Task {self.task.task_id} - {self.comment[:50]}"
        return f"Comment (No Task) - {self.comment[:50]}"