from django.db import models
import uuid



class Task(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    task_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    task_duration = models.DurationField(blank=True, null=True)
    task_comment = models.CharField(max_length=250,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.closed_at:
            self.task_duration = self.closed_at - self.created_at
        super(Task, self).save(*args, **kwargs)


    TASK_TYPE = (
        ('p', 'Production'),
        ('n', 'Non_production')
    )

    type = models.CharField(max_length=1, choices=TASK_TYPE, blank=True, default='p')

    TASK_STATUS = (
        ('w', 'Waiting'),
        ('s', 'Started'),
        ('p', 'Paused'),
        ('c', 'Completed')
    )

    status = models.CharField(max_length=1, choices=TASK_STATUS, blank=True, default='w')


class Comment(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # comment_by = models.CharField(max_length=50) 