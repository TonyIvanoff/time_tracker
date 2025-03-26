
from task_tracker.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.utils import timezone  # Import timezone utilities


def index(request):
    num_tasks = Task.objects.all().count()
    tasks = Task.objects.all()
    
       
    context = {
        'num_tasks' : num_tasks,
        'tasks' : tasks
    }
    
    return render(request, 'task_tracker/index.html', context=context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Comment

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        # Save the comment
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(task=task, comment=comment_text)

        # Update other task fields if needed
        task.type = request.POST.get('type')
        task.status = request.POST.get('status')
        task.task_comment = request.POST.get('task_comment')
        task.save()

        return redirect('task_detail', pk=task.pk)

    comments = task.comment_set.all()  # Fetch all comments for the task
    return render(request, 'task_tracker/task_detail.html', {'task': task, 'comments': comments})